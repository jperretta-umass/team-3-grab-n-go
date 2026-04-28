from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.db import get_db
from app.models_orders import Order
from app.schemas_orders import OrderOut

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/{customer_id}/orders", response_model=List[OrderOut])
def list_customer_orders(
    customer_id: int,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Order).filter(Order.customer_id == customer_id)

    if status == "active":
        query = query.filter(Order.status == "active")
    elif status == "past":
        query = query.filter(Order.status != "active")

    return query.order_by(Order.created_at.desc()).all()


@router.get("/{customer_id}/orders/{order_id}", response_model=OrderOut)
def get_customer_order(
    customer_id: int,
    order_id: int,
    db: Session = Depends(get_db),
):
    order = (
        db.query(Order)
        .filter(Order.customer_id == customer_id, Order.id == order_id)
        .first()
    )
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/{customer_id}/orders/{order_id}/reorder", response_model=OrderOut)
def reorder_customer_order(
    customer_id: int,
    order_id: int,
    db: Session = Depends(get_db),
):
    orig = (
        db.query(Order)
        .filter(Order.customer_id == customer_id, Order.id == order_id)
        .first()
    )
    if orig is None:
        raise HTTPException(status_code=404, detail="Order not found")

    # determine next order_number (simple auto-increment)
    max_num = db.query(func.max(Order.order_number)).scalar()
    try:
        next_num = (int(max_num) + 1) if max_num is not None else 1000
    except Exception:
        next_num = 1000

    new_order = Order(
        customer_id=customer_id,
        order_number=next_num,
        dining_hall=orig.dining_hall,
        pickup_estimate=orig.pickup_estimate,
        status="active",
        status_detail="Preparing",
        items=orig.items,
        total_cents=orig.total_cents,
        created_at=datetime.utcnow(),
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
