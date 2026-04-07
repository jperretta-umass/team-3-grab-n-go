from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.init_db import menu_items
from init_db import init_database
from database import SessionLocal
from sqlalchemy.orm import Session
from models import MenuItems, Cart, CartItem, DiningHall, User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_database()

@app.get("/")
def root():
    return {"message": "Hello"}

@app.get("/menu-items")
def get_menu_items():
    return menu_items

@app.get("/checkout")
def checkout(db: Session, menu_item_ids: list[int]):
     return {"message": "Checkout successful"}