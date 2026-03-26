from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Cart, CartItem, DiningHall, Item
Base.metadata.create_all(bind=engine)


class CartItemUpdate(BaseModel):
    quantity: int

app = FastAPI(root_path="/api")

@app.get("/")
def root():
    return {"message": "Hello"}

@app.get("/")
def root():
    return {"message": "Hello"}


@app.get("/customer/dininghalls")
def list_open_dining_halls(db: Session = Depends(get_db)):
    halls = db.query(DiningHall).filter(DiningHall.is_open.is_(True)).all()
    return halls


@app.get("/customer/dininghalls/items/{dh_id}")
def get_items_for_dining_hall(dh_id: int, db: Session = Depends(get_db)):
    hall = db.query(DiningHall).filter(DiningHall.id == dh_id).first()
    if not hall:
        raise HTTPException(status_code=404, detail="Dining hall not found")

    items = db.query(Item).filter(Item.dining_hall_id == dh_id).all()
    return items


@app.post("/customer/cart/{cart_id}/item/{item_id}")
def add_item_to_cart(cart_id: int, item_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    existing = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart_id, CartItem.item_id == item_id)
        .first()
    )

    if existing:
        existing.quantity += 1
    else:
        existing = CartItem(cart_id=cart_id, item_id=item_id, quantity=1)
        db.add(existing)

    db.commit()
    db.refresh(existing)
    return existing


@app.get("/customer/cart/{cart_id}")
def get_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    items = db.query(CartItem).filter(CartItem.cart_id == cart_id).all()
    return items


@app.delete("/customer/cart/{item_id}")
def remove_item_from_cart(item_id: int, db: Session = Depends(get_db)):
    cart_item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}


@app.patch("/customer/cart/{cart_id}/item/{item_id}")
def update_cart_item_quantity(
    cart_id: int,
    item_id: int,
    payload: CartItemUpdate,
    db: Session = Depends(get_db),
):
    cart_item = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart_id, CartItem.item_id == item_id)
        .first()
    )

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if payload.quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")

    cart_item.quantity = payload.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item