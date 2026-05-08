from contextlib import asynccontextmanager

from fastapi import Body, Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.auth import router as auth_router
from app.database import SessionLocal, get_db
from app.init_db import init_database
from app.models import CurrentOrder, DiningHall, MenuItem, Order, PastOrder, UnclaimedOrder, User
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


@app.post("/api/orders/claim/{order_id}")
def claim_order(order_id: int, db: Session = Depends(get_db)):

    # Find deliverer profile id from demo_delieverer
    deliverer = db.get(User, 2)
    if deliverer is None:
        raise HTTPException(status_code=404, detail="Deliverer not found")

    if deliverer.deliverer_id is None:
        raise HTTPException(status_code=400, detail="User has no deliverer profile")

    # Get the order
    order = db.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    # Checks if the order been claimed
    existing = db.query(CurrentOrder).filter(CurrentOrder.order_id == order_id).first()
    if existing and existing.deliverer_id is not None:
        raise HTTPException(status_code=400, detail="Order already claimed")

    # Check if delieverer claimed an order already
    current_order = (
        db.query(CurrentOrder)
        .filter(CurrentOrder.deliverer_id == deliverer.deliverer_id)
        .first()
    )

    if current_order:
        raise HTTPException(status_code=400, detail="Deliever already claimed an order")

    # Adds it to claimed order
    claimed_order = CurrentOrder(order_id=order_id, deliverer_id=deliverer.deliverer_id)
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
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status

    if status in {"claimed", "on the way"}:
        db.query(UnclaimedOrder).filter(UnclaimedOrder.order_id == order.id).delete()
        existing_current = (
            db.query(CurrentOrder).filter(CurrentOrder.order_id == order.id).first()
        )
        if not existing_current:
            db.add(CurrentOrder(order_id=order.id))

    if status == "delivered":
        db.query(CurrentOrder).filter(CurrentOrder.order_id == order.id).delete()
        db.query(UnclaimedOrder).filter(UnclaimedOrder.order_id == order.id).delete()
        existing_past = db.query(PastOrder).filter(PastOrder.order_id == order.id).first()
        if not existing_past:
            db.add(PastOrder(order_id=order.id))

    db.commit()
    db.refresh(order)
    return {"order": order.to_dict()}
