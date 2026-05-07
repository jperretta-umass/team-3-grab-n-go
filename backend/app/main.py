from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Body, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.auth import router as auth_router
from app.database import get_db
from app.init_db import init_database
from app.models import MenuItem, Order, User, CurrentOrder, UnclaimedOrder
from app.payments import router as payments_router
from app.routers import customer
from fastapi import HTTPException


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
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

app.include_router(payments_router)


@app.get("/")
def root():
    return {"message": "Hello"}


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/api/menu-items")
def get_menu_items(db: Session = Depends(get_db)):
    menu_items = db.query(MenuItem).all()
    return {"menu_items": [item.to_dict() for item in menu_items]}


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
    claimed_order = CurrentOrder(
        order_id = order_id,
        deliverer_id = deliverer.deliverer_id
    )
    # Remove it from unclaimed order
    unclaimed_order = (
        db.query(UnclaimedOrder)
        .filter(UnclaimedOrder.order_id == order_id)
        .first()
    )
    if unclaimed_order:
        db.delete(unclaimed_order)

    db.add(claimed_order)
    db.commit()

    db.refresh(claimed_order)

    return {"message": "Order claimed"}