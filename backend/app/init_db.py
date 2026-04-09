from app.database import MockSession, Base, engine
from app.models import User, DiningHall, MenuItems, Cart, CartItem

db = MockSession()
def init_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    try: 
        hampshire = DiningHall(name='Hampshire', is_open=True)
        berkshire = DiningHall(name='Berkshire', is_open=True)
        franklin = DiningHall(name='Franklin', is_open=True)
        worcester = DiningHall(name='Worcester', is_open=True)
        db.add_all([hampshire, berkshire, franklin, worcester])
        db.flush()

        mock_items = [
            {"name": 'Grilled Chicken Bowl', "mealType": ['dinner'], "diets": ['gluten-free'], "category": 'entree', "diningHall": hampshire, "price": 13.00},
            {"name": 'Veggie Wrap', "mealType": ['lunch'], "diets": ['vegetarian'], "category": 'entree', "diningHall": berkshire, "price": 10.00},
            {"name": 'Tofu Rice Plate', "mealType": ['dinner'], "diets": ['vegan', 'gluten-free'], "category": 'entree', "diningHall": franklin, "price": 12.00},
            {"name": 'Egg Sandwich', "mealType": ['breakfast'], "diets": ['vegetarian'], "category": 'entree', "diningHall": worcester, "price": 8.00},
            {"name": 'Turkey Panini', "mealType": ['lunch'], "diets": ['no-peanuts'], "category": 'entree', "diningHall": hampshire, "price": 11.00},
            {"name": 'Pasta Primavera', "mealType": ['dinner'], "diets": ['vegetarian'], "category": 'entree', "diningHall": hampshire, "price": 12.50},
            {"name": 'Breakfast Burrito', "mealType": ['breakfast'], "diets": ['no-peanuts'], "category": 'entree', "diningHall": hampshire, "price": 9.00},
            {"name": 'Fruit Cup', "mealType": ['breakfast', 'lunch'], "diets": ['vegan', 'gluten-free'], "category": 'snack', "diningHall": hampshire, "price": 3.00}

        ]

        for item in mock_items:
            menu_item = MenuItems(
                name=item['name'],
                meal_type=item['mealType'],
                diets=item['diets'],
                category=item['category'],
                price=item['price'],
                dining_hall=item['diningHall']
            )
            db.add(menu_item)

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error initializing database: {e}")


if __name__ == '__main__':
    init_database()

#menu_items = [
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