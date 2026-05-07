import os
from datetime import datetime, timezone
from typing import Any, Dict, List

import stripe
from app.database import get_db
from app.models import Cart, CartItem, MenuItem, Order, OrderItem
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/payments", tags=["payments"])


def get_secret(env_var: str):
    file_path = os.environ.get(f"{env_var}_FILE")
    if file_path and os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read().strip()
    return os.environ.get(env_var)


stripe.api_key = get_secret("STRIPE_SECRET_KEY")
webhook_secret = get_secret("STRIPE_WEBHOOK_SECRET")


class CartItemRequest(BaseModel):
    menu_item_id: int
    quantity: int = 1


class CheckoutRequest(BaseModel):
    user_id: int
    items: List[CartItemRequest]


@router.post("/create-checkout-session")
def create_checkout_session(request: CheckoutRequest, db: Session = Depends(get_db)):
    try:
        # 1)) Clean up any abandoned carts for this user
        db.query(CartItem).filter(CartItem.cart.has(user_id=request.user_id)).delete()
        db.query(Cart).filter(Cart.user_id == request.user_id).delete()
        db.commit()

        # 2. Save the new cart to the database
        cart = Cart(user_id=request.user_id)
        db.add(cart)
        db.flush()

        line_items: List[Dict[str, Any]] = []
        for item in request.items:
            menu_item = (
                db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
            )
            if not menu_item:
                continue

            # Save the item to the DB cart
            cart_item = CartItem(
                cart_id=cart.id, menu_item_id=menu_item.id, quantity=item.quantity
            )
            db.add(cart_item)

            line_items.append(
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": menu_item.name},
                        "unit_amount": int(menu_item.price * 100),
                    },
                    "quantity": item.quantity,
                }
            )

        db.commit()

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,  # type: ignore
            mode="payment",
            metadata={"user_id": str(request.user_id)},
            success_url="http://localhost/success",
            cancel_url="http://localhost/ItemPage",
        )

        return {"url": checkout_session.url}

    except Exception as e:
        return {"error": str(e)}


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload: bytes = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not sig_header or not webhook_secret:
        raise HTTPException(status_code=400, detail="Missing signature or secret")

    try:
        event = stripe.Webhook.construct_event(  # type: ignore
            payload, sig_header, webhook_secret
        )  # type: ignore
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Listen for successful payment
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = int(session["metadata"]["user_id"])

        # 1. Find the cart  saved earlier
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()

        if cart and cart.items:
            # Grab dining hall from the first item
            hall_id = cart.items[0].menu_item.dining_hall_id

            # Create the  Order
            new_order = Order(
                user_id=user_id,
                dining_hall_id=hall_id,
                total_price=session["amount_total"] / 100,
                status="paid",
                created_at=datetime.now(timezone.utc),
            )
            db.add(new_order)
            db.flush()

            # Move items from CartItem to OrderItem
            for c_item in cart.items:
                o_item = OrderItem(
                    order_id=new_order.id,
                    menu_item_id=c_item.menu_item_id,
                    quantity=c_item.quantity,
                )
                db.add(o_item)

            # Destroy cart
            db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
            db.query(Cart).filter(Cart.id == cart.id).delete()
            db.commit()

    return {"status": "success"}
