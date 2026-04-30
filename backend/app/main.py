from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Body, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.auth import router as auth_router
from app.database import get_db
from app.init_db import init_database
from app.models import MenuItem, Order
from app.routers import customer


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


@app.on_event("startup")
def startup_event():
    init_database()


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


@app.post("/api/orders")
def create_order(
    user_id: int = Body(...),
    dining_hall_id: int = Body(...),
    total_price: float = Body(...),
    status: str = Body(...),
    db: Session = Depends(get_db),
):
    new_order = Order(
        user_id=user_id,
        dining_hall_id=dining_hall_id,
        total_price=total_price,
        status=status,
        created_at=datetime.now(timezone.utc),
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"message": "Order committed successfully", "order": new_order.to_dict()}
