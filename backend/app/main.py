from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import get_db
from app.init_db import init_database
from app.models import MenuItem, Order
from app.routers import customer

app = FastAPI(title="Grab & Go Mock API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
