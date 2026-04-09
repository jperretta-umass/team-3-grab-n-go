from fastapi import FastAPI
from . import db
from init_db import init_database
from models import MenuItems, Order

app = FastAPI()

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
def get_menu_items(db):
    menu_items = db.session.query(MenuItems).all()
    return {"menu_items": [item.to_dict() for item in menu_items]}

@app.post("/api/menu-items")
def commit_order(db, Order):
    db.session.add(Order)
    db.session.commit()
    return {"message": "Order committed successfully"}