from fastapi import FastAPI
from . import menu_items

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello"}

@app.get("/menu-items")
def get_menu_items():
    return menu_items