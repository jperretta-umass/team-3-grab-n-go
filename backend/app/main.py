<<<<<<< HEAD
<<<<<<< HEAD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from app.init_db import init_database, db
from app.models import MenuItems, Order
=======
<<<<<<< HEAD
=======

<<<<<<< HEAD
>>>>>>> 7ed9756 (complete db overhaul fixed)
=======

>>>>>>> 61b152e (quick adjustments to some bugs)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from . import db
from init_db import init_database
from models import MenuItems, Order
<<<<<<< HEAD
>>>>>>> 5a4d67d (order skeleton maybe)
>>>>>>> 2000d26 (order skeleton maybe)
=======

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



>>>>>>> 7ed9756 (complete db overhaul fixed)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def init_db():
    init_database()

@app.get("/")
def root():
    return {"message": "Hello"}

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/api/menu-items")
<<<<<<< HEAD
def get_menu_items():
    menu_items = db.query(MenuItems).all()
    return {"menu_items": [item.to_dict() for item in menu_items]}

@app.post("/api/menu-items")
def commit_order(Order):
    order = Order(
        user_id=Order.user_id,
        total_price=Order.total_price,
        created_at=Order.created_at,
        dining_hall_id=Order.dining_hall_id
    )
    db.add(Order)
    db.commit()
    return {"message": "Order committed successfully"}

@app.get("/api/DelivererPage")
def get_orders():
    orders = db.query(Order).all()
    return {"orders": [order.to_dict() for order in orders]}

=======
def get_menu_items(db):
    menu_items = db.session.query(MenuItems).all()
    return {"menu_items": [item.to_dict() for item in menu_items]}

@app.post("/api/menu-items")
def commit_order(db, Order):
    db.session.add(Order)
    db.session.commit()
    return {"message": "Order committed successfully"}
>>>>>>> 2000d26 (order skeleton maybe)
