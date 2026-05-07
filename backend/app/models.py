"""
FOR FUTURE DEVELOPMENT:

This schema is currently a reference implementation
used to support the testing framework.

If you modify:
- table structure
- relationships
- required fields

You MUST update:
- seed_test_data() in tests/conftest.py
- tests in tests/test_user_profiles.py
- tests in tests/test_customer_api.py

The current test suite assumes:
- specific relationships between User, CustomerProfile, DelivererProfile
"""

from datetime import datetime
from typing import List

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password_hash = mapped_column(String, nullable=False)
    phone_num: Mapped[str] = mapped_column(String, nullable=True)
    has_deliverer_profile: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    deliverer_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("deliverer_profiles.id"),
        nullable=True,
    )

    customer_profile = relationship(
        "CustomerProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        foreign_keys="CustomerProfile.user_id",
    )

    deliverer_profile = relationship(
        "DelivererProfile",
        back_populates="user",
        uselist=False,
        foreign_keys=[deliverer_id],
    )


class CustomerProfile(Base):
    __tablename__ = "customer_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )
    current_order_id: Mapped[int] = mapped_column(Integer, nullable=True)
    past_order_id: Mapped[int] = mapped_column(Integer, nullable=True)

    user = relationship(
        "User",
        back_populates="customer_profile",
        foreign_keys=[user_id],
    )


class DelivererProfile(Base):
    __tablename__ = "deliverer_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    past_order_id: Mapped[int] = mapped_column(Integer, nullable=True)
    current_order_id: Mapped[int] = mapped_column(Integer, nullable=True)

    user = relationship(
        "User",
        back_populates="deliverer_profile",
        uselist=False,
        foreign_keys="User.deliverer_id",
    )


class DiningHall(Base):
    __tablename__ = "dining_halls"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    is_open: Mapped[bool] = mapped_column(Boolean, default=True)
    menu_items: Mapped[List["MenuItem"]] = relationship(
        "MenuItem", back_populates="dining_hall"
    )


class MenuItem(Base):
    __tablename__ = "menu_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    meal_type: Mapped[List[str]] = mapped_column(JSON, nullable=False)
    diets: Mapped[List[str]] = mapped_column(JSON, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    dining_hall_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("dining_halls.id"), nullable=False
    )
    dining_hall: Mapped[DiningHall] = relationship(
        "DiningHall", back_populates="menu_items"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "mealType": self.meal_type,
            "diets": self.diets,
            "category": self.category,
            "price": self.price,
            "dining_hall": self.dining_hall.name if self.dining_hall else None,
        }


class Cart(Base):
    __tablename__ = "carts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    user: Mapped[User] = relationship("User")
    items: Mapped[List["CartItem"]] = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = "cart_items"
    cart_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("carts.id"), primary_key=True
    )
    menu_item_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("menu_items.id"), primary_key=True
    )
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    cart: Mapped[Cart] = relationship("Cart", back_populates="items")
    menu_item: Mapped[MenuItem] = relationship("MenuItem")


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    dining_hall_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("dining_halls.id"), nullable=False
    )
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    delivery_address: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    user: Mapped[User] = relationship("User")
    dining_hall: Mapped[DiningHall] = relationship("DiningHall")
    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "dining_hall_id": self.dining_hall_id,
            "dining_hall": self.dining_hall.name if self.dining_hall else None,
            "total_price": self.total_price,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "items": [
                {
                    "menu_item_id": item.menu_item_id,
                    "quantity": item.quantity,
                }
                for item in self.items
            ],
        }


class OrderItem(Base):
    __tablename__ = "order_items"
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id"), primary_key=True
    )
    menu_item_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("menu_items.id"), primary_key=True
    )
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    special_instructions: Mapped[str] = mapped_column(String, nullable=True)
    delivery_instructions: Mapped[str] = mapped_column(String, nullable=True)
    order: Mapped[Order] = relationship("Order", back_populates="items")
    menu_item: Mapped[MenuItem] = relationship("MenuItem")


class PastOrder(Base):
    __tablename__ = "past_orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id"), nullable=False, unique=True
    )
    order: Mapped[Order] = relationship("Order")


class UnclaimedOrder(Base):
    __tablename__ = "unclaimed_orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id"), nullable=False, unique=True
    )
    order: Mapped[Order] = relationship("Order")


class CurrentOrder(Base):
    __tablename__ = "current_orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id"), nullable=False, unique=True
    )
    deliverer_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("deliverer_profiles.id"), nullable=True
    )
    order: Mapped[Order] = relationship("Order")
    deliverer: Mapped["DelivererProfile"] = relationship("DelivererProfile")
