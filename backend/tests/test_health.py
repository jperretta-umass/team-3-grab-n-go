# Delete this after SQLAlchemy classes
from typing import List, Optional

from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def test_health():
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_SQLAlchemy_installation():
    address = Address(email_address="thisrealemail@gmail.com")
    assert address.email_address == "thisrealemail@gmail.com"


# Proof of concept: Delete when we add SQLAlchemy Classes


class Base(DeclarativeBase):
    pass


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
