from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CartItemAdd(BaseModel):
    menu_item_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemOut(BaseModel):
    menu_item_id: int
    name: str
    price: float
    quantity: int
    subtotal: float


class CartOut(BaseModel):
    cart_id: int
    user_id: int
    items: List[CartItemOut]
    total: float


class OrderItemIn(BaseModel):
    menu_item_id: int
    quantity: int = 1
    special_instructions: Optional[str] = None
    delivery_instructions: Optional[str] = None


class PlaceOrderIn(BaseModel):
    dining_hall_id: int
    items: List[OrderItemIn]


class OrderItemOut(BaseModel):
    menu_item_id: int
    name: str
    price: float
    quantity: int
    special_instructions: Optional[str] = None
    delivery_instructions: Optional[str] = None


class OrderOut(BaseModel):
    id: int
    dining_hall: str
    total_price: float
    status: str
    created_at: datetime
    items: List[OrderItemOut]
