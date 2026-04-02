from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import get_db
from .init_db import init_database
from .models import MenuItem

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost"],
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
def get_menu_items(db: Session = Depends(get_db)):
    items = db.query(MenuItem).all()

    return [
        {
            "id": item.id,
            "name": item.name,
            "mealType": item.meal_type.split(","),
            "diets": item.diets.split(","),
            "category": item.category,
            "diningHall": item.dining_hall.name,
        }
        for item in items
    ]