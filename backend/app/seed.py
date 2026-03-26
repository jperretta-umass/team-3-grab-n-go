from app.database import SessionLocal
from app.models import Cart, DiningHall, Item, User


def run():
    db = SessionLocal()

    existing_user = db.query(User).filter(User.username == "alice").first()
    if not existing_user:
        user = User(
            username="alice",
            password_hash="demo-password-hash",
            role="customer",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        cart = Cart(user_id=user.id)
        db.add(cart)
        db.commit()

    existing_hall = db.query(DiningHall).filter(DiningHall.name == "Worcester").first()
    if not existing_hall:
        woo = DiningHall(name="Worcester", is_open=True)
        frank = DiningHall(name="Franklin", is_open=True)
        db.add_all([woo, frank])
        db.commit()
        db.refresh(woo)
        db.refresh(frank)

        db.add_all(
            [
                Item(name="Burger", price_cents=899, dining_hall_id=woo.id),
                Item(name="Fries", price_cents=399, dining_hall_id=woo.id),
                Item(name="Salad", price_cents=699, dining_hall_id=frank.id),
            ]
        )
        db.commit()

    db.close()


if __name__ == "__main__":
    run()