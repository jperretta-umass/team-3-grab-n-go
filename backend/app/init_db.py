from datetime import datetime, timezone
from typing import TypedDict

from app.auth import get_password_hash
from app.database import Base, SessionLocal, engine
from app.models import (
    CurrentOrder,
    CustomerProfile,
    DelivererProfile,
    DiningHall,
    MenuItem,
    Order,
    OrderItem,
    PastOrder,
    UnclaimedOrder,
    User,
)


class MockMenuItem(TypedDict):
    name: str
    mealType: list[str]
    diets: list[str]
    category: str
    dining_hall: DiningHall
    price: float


def init_database():
    if SessionLocal is None:
        raise RuntimeError(
            "DATABASE_URL is not set. Set DATABASE_URL before calling init_database()."
        )

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # change i made here to avoid duplicates when running init_db
        # originally dropped all tables but this guard should protect the app
        def get_or_create_dining_hall(name: str) -> DiningHall:
            dining_hall = db.query(DiningHall).filter(DiningHall.name == name).first()
            if dining_hall is None:
                dining_hall = DiningHall(name=name, is_open=True)
                db.add(dining_hall)
                db.flush()
            return dining_hall

        hampshire = get_or_create_dining_hall("Hampshire")
        berkshire = get_or_create_dining_hall("Berkshire")
        franklin = get_or_create_dining_hall("Franklin")
        worcester = get_or_create_dining_hall("Worcester")

        mock_items: list[MockMenuItem] = [
            {
                "name": "Grilled Chicken Bowl",
                "mealType": ["dinner"],
                "diets": ["gluten-free"],
                "category": "entree",
                "dining_hall": hampshire,
                "price": 13.00,
            },
            {
                "name": "Veggie Wrap",
                "mealType": ["lunch"],
                "diets": ["vegetarian"],
                "category": "entree",
                "dining_hall": berkshire,
                "price": 10.00,
            },
            {
                "name": "Tofu Rice Plate",
                "mealType": ["dinner"],
                "diets": ["vegan", "gluten-free"],
                "category": "entree",
                "dining_hall": franklin,
                "price": 12.00,
            },
            {
                "name": "Egg Sandwich",
                "mealType": ["breakfast"],
                "diets": ["vegetarian"],
                "category": "entree",
                "dining_hall": worcester,
                "price": 8.00,
            },
            {
                "name": "Turkey Panini",
                "mealType": ["lunch"],
                "diets": ["no-peanuts"],
                "category": "entree",
                "dining_hall": hampshire,
                "price": 11.00,
            },
            {
                "name": "Pasta Primavera",
                "mealType": ["dinner"],
                "diets": ["vegetarian"],
                "category": "entree",
                "dining_hall": hampshire,
                "price": 12.50,
            },
            {
                "name": "Breakfast Burrito",
                "mealType": ["breakfast"],
                "diets": ["no-peanuts"],
                "category": "entree",
                "dining_hall": hampshire,
                "price": 9.00,
            },
            {
                "name": "Fruit Cup",
                "mealType": ["breakfast", "lunch"],
                "diets": ["vegan", "gluten-free"],
                "category": "snack",
                "dining_hall": hampshire,
                "price": 3.00,
            },
        ]

        for item in mock_items:
            exists = (
                # second guard i added to avoid duplicate menu items
                db.query(MenuItem)
                .filter(
                    MenuItem.name == item["name"],
                    MenuItem.dining_hall_id == item["dining_hall"].id,
                )
                .first()
            )
            if not exists:
                menu_item = MenuItem(
                    name=item["name"],
                    meal_type=item["mealType"],
                    diets=item["diets"],
                    category=item["category"],
                    price=item["price"],
                    dining_hall=item["dining_hall"],
                )
                db.add(menu_item)
        db.flush()

        demo_customer = db.query(User).filter(User.username == "demo_customer").first()
        if demo_customer is None:
            demo_customer = User(
                username="demo_customer",
                email="demo_customer@example.com",
                password_hash=get_password_hash("string3214"),
                phone_num="555-0100",
                has_deliverer_profile=False,
            )
            db.add(demo_customer)
            db.flush()

        customer_profile = (
            db.query(CustomerProfile)
            .filter(CustomerProfile.user_id == demo_customer.id)
            .first()
        )
        if customer_profile is None:
            db.add(CustomerProfile(user_id=demo_customer.id))
            db.flush()

        demo_deliverer = (
            db.query(User).filter(User.username == "demo_deliverer").first()
        )
        if demo_deliverer is None:
            demo_deliverer = User(
                username="demo_deliverer",
                email="demo_deliverer@example.com",
                password_hash=get_password_hash("string3214"),
                phone_num="555-0100",
                has_deliverer_profile=True,
            )
            db.add(demo_deliverer)
            db.flush()

        two_role_profile = (
            db.query(CustomerProfile)
            .filter(CustomerProfile.user_id == demo_deliverer.id)
            .first()
        )
        if two_role_profile is None:
            db.add(CustomerProfile(user_id=demo_deliverer.id))
            db.flush()

        # final guard i added, adds demo orders only if no orders in existence
        existing_orders = (
            db.query(Order).filter(Order.user_id == demo_customer.id).first()
        )
        if existing_orders is None:

            breakfast_burrito = (
                db.query(MenuItem).filter(MenuItem.name == "Breakfast Burrito").first()
            )
            veggie_wrap = (
                db.query(MenuItem).filter(MenuItem.name == "Veggie Wrap").first()
            )
            fruit_cup = db.query(MenuItem).filter(MenuItem.name == "Fruit Cup").first()

            if breakfast_burrito is None:
                raise RuntimeError("Failed to seed Breakfast Burrito menu item")

            # Seed a past (completed) order
            past_order = Order(
                user_id=demo_customer.id,
                dining_hall_id=breakfast_burrito.dining_hall_id,
                total_price=breakfast_burrito.price * 2,
                status="completed",
                created_at=datetime(2026, 4, 20, 12, 0, 0),
            )
            db.add(past_order)
            db.flush()
            db.add(
                OrderItem(
                    order_id=past_order.id,
                    menu_item_id=breakfast_burrito.id,
                    quantity=2,
                )
            )
            db.add(PastOrder(order_id=past_order.id))

            # Seed an active (in-delivery) order
            active_order = Order(
                user_id=demo_customer.id,
                dining_hall_id=(
                    veggie_wrap.dining_hall_id
                    if veggie_wrap
                    else breakfast_burrito.dining_hall_id
                ),
                total_price=(
                    veggie_wrap.price if veggie_wrap else breakfast_burrito.price
                )
                + (fruit_cup.price if fruit_cup else 0),
                status="active",
                created_at=datetime.now(timezone.utc),
            )
            db.add(active_order)
            db.flush()
            if veggie_wrap:
                db.add(
                    OrderItem(
                        order_id=active_order.id,
                        menu_item_id=veggie_wrap.id,
                        quantity=1,
                    )
                )
            if fruit_cup:
                db.add(
                    OrderItem(
                        order_id=active_order.id, menu_item_id=fruit_cup.id, quantity=1
                    )
                )
            db.add(CurrentOrder(order_id=active_order.id, deliverer_id=None))

            # Seed an unclaimed order
            unclaimed_order = Order(
                user_id=demo_customer.id,
                dining_hall_id=breakfast_burrito.dining_hall_id,
                total_price=breakfast_burrito.price * 3,
                status="unclaimed",
                created_at=datetime.now(timezone.utc),
            )
            db.add(unclaimed_order)
            db.flush()
            db.add(
                OrderItem(
                    order_id=unclaimed_order.id,
                    menu_item_id=breakfast_burrito.id,
                    quantity=3,
                    special_instructions="Extra hot sauce please",
                )
            )
            db.add(UnclaimedOrder(order_id=unclaimed_order.id))

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error initializing database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
