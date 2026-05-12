from contextlib import asynccontextmanager

from fastapi import Body, Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.auth import get_current_user, router as auth_router
from app.database import SessionLocal, get_db
from app.init_db import init_database
from app.models import (
    CurrentOrder,
    DelivererProfile,
    DiningHall,
    MenuItem,
    Order,
    PastOrder,
    UnclaimedOrder,
    User,
)
from app.payments import router as payments_router
from app.routers import customer
from app.routers.dining_menu import router as dining_menu_router
from app.services.menu_sync import sync_today_menu_to_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL is not set")
    db = SessionLocal()
    try:
        await sync_today_menu_to_db(db)
    except Exception as e:
        print(f"Menu sync failed on startup: {e}")
    finally:
        db.close()
    yield


app = FastAPI(title="Grab & Go Mock API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(customer.router)
app.include_router(dining_menu_router)

app.include_router(payments_router)


@app.get("/")
def root():
    return {"message": "Hello"}


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/api/menu-items")
def get_menu_items(
    hall: str | None = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(MenuItem)
    if hall:
        q = q.join(DiningHall).filter(DiningHall.name.ilike(hall))
    return {"menu_items": [item.to_dict() for item in q.all()]}


@app.get("/api/orders")
def get_order(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return {"orders": [order.to_dict() for order in orders]}


def ensure_deliverer_profile(user: User, db: Session) -> int:
    if not user.has_deliverer_profile:
        raise HTTPException(status_code=403, detail="User is not a deliverer")

    if user.deliverer_id is None:
        profile = DelivererProfile()
        db.add(profile)
        db.flush()
        user.deliverer_id = profile.id
        db.add(user)

    return user.deliverer_id


@app.get("/api/orders/deliverer/current")
def get_current_deliverer_order(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deliverer_id = ensure_deliverer_profile(current_user, db)
    current_order = (
        db.query(CurrentOrder)
        .filter(CurrentOrder.deliverer_id == deliverer_id)
        .join(Order)
        .filter(Order.status.in_(["claimed", "on the way"]))
        .first()
    )

    if current_order is None:
        return {"order": None}

    return {"order": current_order.order.to_dict()}


@app.get("/api/orders/deliverer/past")
def get_past_deliverer_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deliverer_id = ensure_deliverer_profile(current_user, db)
    current_orders = (
        db.query(CurrentOrder)
        .filter(CurrentOrder.deliverer_id == deliverer_id)
        .all()
    )
    delivered_orders = [
        current_order.order.to_dict()
        for current_order in current_orders
        if current_order.order.status == "delivered"
    ]
    return {"orders": delivered_orders}


@app.post("/api/orders/claim/{order_id}")
def claim_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deliverer_id = ensure_deliverer_profile(current_user, db)

    # Get the order
    order = db.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "unclaimed":
        raise HTTPException(status_code=400, detail="Order already claimed")

    # Checks if the order been claimed
    existing = db.query(CurrentOrder).filter(CurrentOrder.order_id == order_id).first()
    if existing and existing.deliverer_id is not None:
        raise HTTPException(status_code=400, detail="Order already claimed")

    # Check if deliverer claimed an order already
    current_order = (
        db.query(CurrentOrder)
        .filter(CurrentOrder.deliverer_id == deliverer_id)
        .join(Order)
        .filter(Order.status.in_(["claimed", "on the way"]))
        .first()
    )

    if current_order:
        raise HTTPException(status_code=400, detail="Deliverer already claimed an order")

    # Adds it to claimed order
    claimed_order = CurrentOrder(order_id=order_id, deliverer_id=deliverer_id)
    # Remove it from unclaimed order
    unclaimed_order = (
        db.query(UnclaimedOrder).filter(UnclaimedOrder.order_id == order_id).first()
    )
    if unclaimed_order:
        db.delete(unclaimed_order)

    order.status = "claimed"

    db.add(claimed_order)
    db.commit()
    db.refresh(order)
    return {"message": "Order claimed", "order": order.to_dict()}


@app.patch("/api/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    status: str = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deliverer_id = ensure_deliverer_profile(current_user, db)
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    current_order = (
        db.query(CurrentOrder)
        .filter(
            CurrentOrder.order_id == order_id,
            CurrentOrder.deliverer_id == deliverer_id,
        )
        .first()
    )
    if current_order is None:
        raise HTTPException(
            status_code=403,
            detail="Order is not assigned to this deliverer",
        )

    order.status = status

    if status in {"claimed", "on the way"}:
        db.query(UnclaimedOrder).filter(UnclaimedOrder.order_id == order.id).delete()

    if status == "delivered":
        db.query(UnclaimedOrder).filter(UnclaimedOrder.order_id == order.id).delete()
        existing_past = (
            db.query(PastOrder).filter(PastOrder.order_id == order.id).first()
        )
        if not existing_past:
            db.add(PastOrder(order_id=order.id))

    db.commit()
    db.refresh(order)
    return {"order": order.to_dict()}
