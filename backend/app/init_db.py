from datetime import datetime

from app.database import Base, SessionLocal, engine
from app.models import DiningHall, MenuItem, Order, OrderItem, User


def init_database():
    if SessionLocal is None:
        raise RuntimeError(
            "DATABASE_URL is not set. Set DATABASE_URL before calling init_database()."
        )

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        hampshire = DiningHall(name="Hampshire", is_open=True)
        berkshire = DiningHall(name="Berkshire", is_open=True)
        franklin = DiningHall(name="Franklin", is_open=True)
        worcester = DiningHall(name="Worcester", is_open=True)

        db.add_all([hampshire, berkshire, franklin, worcester])
        db.flush()

        mock_items = [
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

        demo_user = User(
            username="demo_customer",
            email="demo_customer@example.com",
            phone_num="555-0100",
            has_deliverer_profile=False,
        )
        db.add(demo_user)
        db.flush()

        breakfast_burrito = (
            db.query(MenuItem).filter(MenuItem.name == "Breakfast Burrito").first()
        )
        if breakfast_burrito is None:
            raise RuntimeError("Failed to seed Breakfast Burrito menu item")

        quantity = 3
        line_total = breakfast_burrito.price * quantity

        mock_order = Order(
            user_id=demo_user.id,
            dining_hall_id=breakfast_burrito.dining_hall_id,
            total_price=line_total,
            status="pending",
            created_at=datetime.utcnow(),
        )
        db.add(mock_order)
        db.flush()

        mock_order_item = OrderItem(
            order_id=mock_order.id,
            menu_item_id=breakfast_burrito.id,
            quantity=quantity,
        )

        db.add(mock_order_item)

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error initializing database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    init_database()

# menu_items = [
#   {
#     "id": 1,
#     "name": 'Grilled Chicken Bowl',
#     "mealType": ['lunch', 'dinner'],
#     "diets": ['gluten-free'],
#     "category": 'entree',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 2,
#     "name": 'Veggie Wrap',
#     "mealType": ['lunch'],
#     "diets": ['vegetarian'],
#     "category": 'entree',
#     "diningHall": 'Berkshire',
#   },
#   {
#     "id": 3,
#     "name": 'Tofu Rice Plate',
#     "mealType": ['dinner'],
#     "diets": ['vegan', 'gluten-free'],
#     "category": 'entree',
#     "diningHall": 'Franklin',
#   },
#   {
#     "id": 4,
#     "name": 'Egg Sandwich',
#     "mealType": ['breakfast'],
#     "diets": ['vegetarian'],
#     "category": 'entree',
#     "diningHall": 'Worcester',
#   },
#   {
#     "id": 5,
#     "name": 'Turkey Panini',
#     "mealType": ['lunch'],
#     "diets": ['no-peanuts'],
#     "category": 'entree',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 6,
#     "name": 'Pasta Primavera',
#     "mealType": ['dinner'],
#     "diets": ['vegetarian'],
#     "category": 'entree',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 7,
#     "name": 'Breakfast Burrito',
#     "mealType": ['breakfast'],
#     "diets": ['no-peanuts'],
#     "category": 'entree',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 101,
#     "name": 'Fruit Cup',
#     "mealType": ['breakfast', 'lunch', 'dinner'],
#     "diets": ['vegan', 'gluten-free', 'vegetarian', 'no-peanuts'],
#     "category": 'snack',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 102,
#     "name": 'Granola Bar',
#     "mealType": ['breakfast', 'lunch'],
#     "diets": ['vegetarian'],
#     "category": 'snack',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 103,
#     "name": 'Orange Juice',
#     "mealType": ['breakfast'],
#     "diets": ['vegan', 'gluten-free', 'vegetarian', 'no-peanuts'],
#     "category": 'drink',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 104,
#     "name": 'Iced Tea',
#     "mealType": ['lunch', 'dinner'],
#     "diets": ['vegan', 'gluten-free', 'vegetarian', 'no-peanuts'],
#     "category": 'drink',
#     "diningHall": 'Berkshire',
#   },
#   {
#     "id": 105,
#     "name": 'Yogurt Cup',
#     "mealType": ['breakfast', 'lunch'],
#     "diets": ['vegetarian', 'gluten-free'],
#     "category": 'snack',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 106,
#     "name": 'Trail Mix',
#     "mealType": ['lunch', 'dinner'],
#     "diets": ['vegetarian'],
#     "category": 'snack',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 107,
#     "name": 'Sparkling Water',
#     "mealType": ['breakfast', 'lunch', 'dinner'],
#     "diets": ['vegan', 'gluten-free', 'vegetarian', 'no-peanuts'],
#     "category": 'drink',
#     "diningHall": 'Hampshire',
#   },
# ]

# menu_items = [
#   {
#     "id": 1,
#     "name": 'Grilled Chicken Bowl',
#     "mealType": ['lunch', 'dinner'],
#     "diets": ['gluten-free'],
#     "category": 'entree',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 2,
#     "name": 'Veggie Wrap',
#     "mealType": ['lunch'],
#     "diets": ['vegetarian'],
#     "category": 'entree',
#     "diningHall": 'Berkshire',
#   },
#   {
#     "id": 3,
#     "name": 'Tofu Rice Plate',
#     "mealType": ['dinner'],
#     "diets": ['vegan', 'gluten-free'],
#     "category": 'entree',
#     "diningHall": 'Franklin',
#   },
#   {
#     "id": 4,
#     "name": 'Egg Sandwich',
#     "mealType": ['breakfast'],
#     "diets": ['vegetarian'],
#     "category": 'entree',
#     "diningHall": 'Worcester',
#   },
#   {
#     "id": 5,
#     "name": 'Turkey Panini',
#     "mealType": ['lunch'],
#     "diets": ['no-peanuts'],
#     "category": 'entree',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 6,
#     "name": 'Pasta Primavera',
#     "mealType": ['dinner'],
#     "diets": ['vegetarian'],
#     "category": 'entree',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 7,
#     "name": 'Breakfast Burrito',
#     "mealType": ['breakfast'],
#     "diets": ['no-peanuts'],
#     "category": 'entree',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 101,
#     "name": 'Fruit Cup',
#     "mealType": ['breakfast', 'lunch', 'dinner'],
#     "diets": ['vegan', 'gluten-free', 'vegetarian', 'no-peanuts'],
#     "category": 'snack',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 102,
#     "name": 'Granola Bar',
#     "mealType": ['breakfast', 'lunch'],
#     "diets": ['vegetarian'],
#     "category": 'snack',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 103,
#     "name": 'Orange Juice',
#     "mealType": ['breakfast'],
#     "diets": ['vegan', 'gluten-free', 'vegetarian', 'no-peanuts'],
#     "category": 'drink',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 104,
#     "name": 'Iced Tea',
#     "mealType": ['lunch', 'dinner'],
#     "diets": ['vegan', 'gluten-free', 'vegetarian', 'no-peanuts'],
#     "category": 'drink',
#     "diningHall": 'Berkshire',
#   },
#   {
#     "id": 105,
#     "name": 'Yogurt Cup',
#     "mealType": ['breakfast', 'lunch'],
#     "diets": ['vegetarian', 'gluten-free'],
#     "category": 'snack',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 106,
#     "name": 'Trail Mix',
#     "mealType": ['lunch', 'dinner'],
#     "diets": ['vegetarian'],
#     "category": 'snack',
#     "diningHall": 'Hampshire',
#   },
#   {
#     "id": 107,
#     "name": 'Sparkling Water',
#     "mealType": ['breakfast', 'lunch', 'dinner'],
#     "diets": ['vegan', 'gluten-free', 'vegetarian', 'no-peanuts'],
#     "category": 'drink',
#     "diningHall": 'Hampshire',
#   },
# ]
