from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import menu_items

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello"}

@app.get("/menu-items")
def get_menu_items():
    return menu_items