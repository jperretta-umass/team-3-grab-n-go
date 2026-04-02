from .database import engine, SessionLocal, Base
from .models import DiningHall, MenuItem


def init_database():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(MenuItem).count() > 0:
            return

        hampshire = DiningHall(name="Hampshire", is_open=True)
        berkshire = DiningHall(name="Berkshire", is_open=True)
        franklin = DiningHall(name="Franklin", is_open=True)
        worcester = DiningHall(name="Worcester", is_open=True)

        db.add_all([hampshire, berkshire, franklin, worcester])
        db.flush()

        mock_items = [
            {"name": "Grilled Chicken Bowl", "mealType": ["lunch", "dinner"], "diets": ["gluten-free"], "category": "entree", "diningHall": hampshire, "price": 13.00},
            {"name": "Veggie Wrap", "mealType": ["lunch"], "diets": ["vegetarian"], "category": "entree", "diningHall": berkshire, "price": 10.00},
            {"name": "Tofu Rice Plate", "mealType": ["dinner"], "diets": ["vegan", "gluten-free"], "category": "entree", "diningHall": franklin, "price": 12.00},
            {"name": "Egg Sandwich", "mealType": ["breakfast"], "diets": ["vegetarian"], "category": "entree", "diningHall": worcester, "price": 8.00},
            {"name": "Turkey Panini", "mealType": ["lunch"], "diets": ["no-peanuts"], "category": "entree", "diningHall": hampshire, "price": 11.00},
            {"name": "Pasta Primavera", "mealType": ["dinner"], "diets": ["vegetarian"], "category": "entree", "diningHall": hampshire, "price": 12.50},
            {"name": "Breakfast Burrito", "mealType": ["breakfast"], "diets": ["no-peanuts"], "category": "entree", "diningHall": hampshire, "price": 9.00},
            {"name": "Fruit Cup", "mealType": ["breakfast", "lunch", "dinner"], "diets": ["vegan", "gluten-free", "vegetarian", "no-peanuts"], "category": "snack", "diningHall": hampshire, "price": 3.00},
            {"name": "Granola Bar", "mealType": ["breakfast", "lunch"], "diets": ["vegetarian"], "category": "snack", "diningHall": hampshire, "price": 3.00},
            {"name": "Orange Juice", "mealType": ["breakfast"], "diets": ["vegan", "gluten-free", "vegetarian", "no-peanuts"], "category": "drink", "diningHall": hampshire, "price": 3.00},
        ]

        for item in mock_items:
            menu_item = MenuItem(
                name=item["name"],
                meal_type=",".join(item["mealType"]),
                diets=",".join(item["diets"]),
                category=item["category"],
                price=item["price"],
                dining_hall=item["diningHall"],
            )
            db.add(menu_item)

        db.commit()
    finally:
        db.close()