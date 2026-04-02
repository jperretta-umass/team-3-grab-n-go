"""
FOR FUTURE DEVELOPMENT:

This schema is currently a reference implementation used to support the testing framework.

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
- existence of DiningHall, Item, Cart, CartItem tables
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    phone_num = Column(String, nullable=True)
    has_deliverer_profile = Column(Boolean, nullable=False, default=False)
    deliverer_id = Column(Integer, ForeignKey("deliverer_profiles.id"), nullable=True)

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

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    current_order_id = Column(Integer, nullable=True)
    past_order_id = Column(Integer, nullable=True)

    user = relationship(
        "User",
        back_populates="customer_profile",
        foreign_keys=[user_id],
    )


class DelivererProfile(Base):
    __tablename__ = "deliverer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    past_order_id = Column(Integer, nullable=True)
    current_order_id = Column(Integer, nullable=True)

    user = relationship(
        "User",
        back_populates="deliverer_profile",
        uselist=False,
        foreign_keys="User.deliverer_id",
    )


class DiningHall(Base):
    __tablename__ = "dining_halls"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_open = Column(Boolean, nullable=False, default=True)

    items = relationship("Item", back_populates="dining_hall")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price_cents = Column(Integer, nullable=False)
    dining_hall_id = Column(Integer, ForeignKey("dining_halls.id"), nullable=False)

    dining_hall = relationship("DiningHall", back_populates="items")


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan",
    )


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    cart = relationship("Cart", back_populates="items")