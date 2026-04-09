from fastapi import FastAPI
from database import db
from init_db import init_database
from models import MenuItems

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
def get_menu_items():
    menu_items = db.session.query(MenuItems).all()
    return {"menu_items": [item.to_dict() for item in menu_items]}