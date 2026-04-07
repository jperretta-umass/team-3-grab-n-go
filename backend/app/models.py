from . import db
from typing import List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(db.model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

class DiningHall(db.model):
    __tablename__ = 'dining_halls'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    is_open: Mapped[bool] = mapped_column(Boolean, default=True)
    menu_items: Mapped[List['MenuItems']] = relationship('MenuItems', back_populates='dining_hall')

class MenuItems(db.model):
    __tablename__ = 'menu_items'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    meal_type: Mapped[List[str]] = mapped_column(JSON, nullable=False)
    diets: Mapped[List[str]] = mapped_column(JSON, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    dining_hall_id: Mapped[int] = mapped_column(Integer, ForeignKey('dining_halls.id'), nullable=False)
    dining_hall: Mapped[DiningHall] = relationship('DiningHall', back_populates='menu_items')

class Cart(db.model):
    __tablename__ = 'carts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    user: Mapped[User] = relationship('User')
    items: Mapped[List['CartItem']] = relationship('CartItem', back_populates='cart')

class CartItem(db.model):
    __tablename__ = 'cart_items'
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey('carts.id'), primary_key=True)
    menu_item_id: Mapped[int] = mapped_column(Integer, ForeignKey('menu_items.id'), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    cart: Mapped[List[Cart]] = relationship('Cart', back_populates='items')
    menu_item: Mapped[MenuItems] = relationship('MenuItems')