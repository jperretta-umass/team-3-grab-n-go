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

from app.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    phone_num = Column(String, nullable=True)
    has_deliverer_profile = Column(Boolean, nullable=False, default=False)
    deliverer_id = Column(
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

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )
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
