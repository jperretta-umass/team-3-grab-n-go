from datetime import datetime, timezone
from typing import List

from app.database import get_db
from app.models import (
    Cart,
    CartItem,
    CurrentOrder,
    DiningHall,
    MenuItem,
    Order,
    OrderItem,
    PastOrder,
    UnclaimedOrder,
    User,
)
from app.schemas_customer import (
    CartItemAdd,
    CartItemOut,
    CartItemUpdate,
    CartOut,
    OrderItemIn,
    OrderItemOut,
    OrderOut,
    PlaceOrderIn,
)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/customers", tags=["customers"])


def _get_user_or_404(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def _get_or_create_cart(user_id: int, db: Session) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.flush()
    return cart


def _order_to_out(order: Order) -> OrderOut:
    return OrderOut(
        id=order.id,
        dining_hall=(
            order.dining_hall.name if order.dining_hall else str(order.dining_hall_id)
        ),
        total_price=order.total_price,
        status=order.status,
        created_at=order.created_at,
        items=[
            OrderItemOut(
                menu_item_id=oi.menu_item_id,
                name=oi.menu_item.name if oi.menu_item else str(oi.menu_item_id),
                price=oi.menu_item.price if oi.menu_item else 0.0,
                quantity=oi.quantity,
                special_instructions=oi.special_instructions,
                delivery_instructions=oi.delivery_instructions,
            )
            for oi in order.items
        ],
    )


def _cart_to_out(cart: Cart) -> CartOut:
    items_out: List[CartItemOut] = []
    total = 0.0
    for ci in cart.items:
        subtotal = ci.menu_item.price * ci.quantity
        total += subtotal
        items_out.append(
            CartItemOut(
                menu_item_id=ci.menu_item_id,
                name=ci.menu_item.name,
                price=ci.menu_item.price,
                quantity=ci.quantity,
                subtotal=subtotal,
            )
        )
    return CartOut(
        cart_id=cart.id, user_id=cart.user_id, items=items_out, total=round(total, 2)
    )


@router.get("/{user_id}/profile")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = _get_user_or_404(user_id, db)

    active_count = (
        db.query(CurrentOrder)
        .join(Order, CurrentOrder.order_id == Order.id)
        .filter(Order.user_id == user_id)
        .count()
    )
    past_count = (
        db.query(PastOrder)
        .join(Order, PastOrder.order_id == Order.id)
        .filter(Order.user_id == user_id)
        .count()
    )

    return {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "phone_num": user.phone_num,
        "has_deliverer_profile": user.has_deliverer_profile,
        "active_orders_count": active_count,
        "past_orders_count": past_count,
    }


@router.get("/{user_id}/active-orders", response_model=List[OrderOut])
def get_active_orders(user_id: int, db: Session = Depends(get_db)):
    _get_user_or_404(user_id, db)

    orders = (
        db.query(Order)
        .join(CurrentOrder, CurrentOrder.order_id == Order.id)
        .filter(Order.user_id == user_id)
        .all()
    )
    return [_order_to_out(o) for o in orders]


@router.get("/{user_id}/past-orders", response_model=List[OrderOut])
def get_past_orders(user_id: int, db: Session = Depends(get_db)):
    _get_user_or_404(user_id, db)

    orders = (
        db.query(Order)
        .join(PastOrder, PastOrder.order_id == Order.id)
        .filter(Order.user_id == user_id)
        .all()
    )
    return [_order_to_out(o) for o in orders]


@router.get("/{user_id}/orders", response_model=List[OrderOut])
def get_orders_for_user(user_id: int, db: Session = Depends(get_db)):
    _get_user_or_404(user_id, db)

    orders = (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return [_order_to_out(o) for o in orders]


@router.post("/{user_id}/orders", response_model=OrderOut, status_code=201)
def place_order(user_id: int, body: PlaceOrderIn, db: Session = Depends(get_db)):
    _get_user_or_404(user_id, db)

    dh = db.query(DiningHall).filter(DiningHall.id == body.dining_hall_id).first()
    if not dh:
        raise HTTPException(status_code=404, detail="Dining hall not found")

    total = 0.0
    resolved: List[tuple[MenuItem, OrderItemIn]] = []
    for item_in in body.items:
        mi = db.query(MenuItem).filter(MenuItem.id == item_in.menu_item_id).first()
        if not mi:
            raise HTTPException(
                status_code=404, detail=f"Menu item {item_in.menu_item_id} not found"
            )
        total += mi.price * item_in.quantity
        resolved.append((mi, item_in))

    order = Order(
        user_id=user_id,
        dining_hall_id=body.dining_hall_id,
        total_price=round(total, 2),
        status="unclaimed",
        created_at=datetime.now(timezone.utc),
    )
    db.add(order)
    db.flush()

    for mi, item_in in resolved:
        db.add(
            OrderItem(
                order_id=order.id,
                menu_item_id=mi.id,
                quantity=item_in.quantity,
                special_instructions=item_in.special_instructions,
                delivery_instructions=item_in.delivery_instructions,
            )
        )

    db.add(UnclaimedOrder(order_id=order.id))
    db.commit()
    db.refresh(order)
    return _order_to_out(order)


@router.get("/{user_id}/cart", response_model=CartOut)
def get_cart(user_id: int, db: Session = Depends(get_db)):
    _get_user_or_404(user_id, db)
    cart = _get_or_create_cart(user_id, db)
    db.commit()
    return _cart_to_out(cart)


@router.post("/{user_id}/cart/items", response_model=CartOut, status_code=201)
def add_cart_item(user_id: int, body: CartItemAdd, db: Session = Depends(get_db)):
    _get_user_or_404(user_id, db)

    mi = db.query(MenuItem).filter(MenuItem.id == body.menu_item_id).first()
    if not mi:
        raise HTTPException(status_code=404, detail="Menu item not found")

    cart = _get_or_create_cart(user_id, db)

    existing = (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart.id,
            CartItem.menu_item_id == body.menu_item_id,
        )
        .first()
    )

    if existing:
        existing.quantity += body.quantity
    else:
        db.add(
            CartItem(
                cart_id=cart.id, menu_item_id=body.menu_item_id, quantity=body.quantity
            )
        )

    db.commit()
    db.refresh(cart)
    return _cart_to_out(cart)


@router.put("/{user_id}/cart/items/{menu_item_id}", response_model=CartOut)
def update_cart_item(
    user_id: int, menu_item_id: int, body: CartItemUpdate, db: Session = Depends(get_db)
):
    _get_user_or_404(user_id, db)
    cart = _get_or_create_cart(user_id, db)

    item = (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart.id,
            CartItem.menu_item_id == menu_item_id,
        )
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not in cart")

    if body.quantity <= 0:
        db.delete(item)
    else:
        item.quantity = body.quantity

    db.commit()
    db.refresh(cart)
    return _cart_to_out(cart)


@router.delete("/{user_id}/cart/items/{menu_item_id}", response_model=CartOut)
def remove_cart_item(user_id: int, menu_item_id: int, db: Session = Depends(get_db)):
    _get_user_or_404(user_id, db)
    cart = _get_or_create_cart(user_id, db)

    item = (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart.id,
            CartItem.menu_item_id == menu_item_id,
        )
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not in cart")

    db.delete(item)
    db.commit()
    db.refresh(cart)
    return _cart_to_out(cart)
