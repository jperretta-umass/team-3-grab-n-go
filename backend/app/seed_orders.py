import json
from datetime import datetime

from sqlalchemy import text

from app.db import SessionLocal, create_tables, engine
from app.models_orders import Order


def seed() -> None:
    # drop orders table if it exists so schema changes apply cleanly
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS orders"))

    # create tables with current models
    create_tables()

    db = SessionLocal()
    try:
        orders = [
            Order(
                customer_id=1,
                order_number=1024,
                dining_hall="Hampshire",
                pickup_estimate="10-15 min",
                status_detail="Preparing",
                status="active",
                items=json.dumps({"items": [{"name": "Grilled Chicken Bowl", "qty": 1}, {"name": "Fruit Cup", "qty": 1}]}),
                total_cents=1298,
                created_at=datetime.utcnow(),
            ),
            Order(
                customer_id=1,
                order_number=1018,
                dining_hall="Berkshire",
                pickup_estimate=None,
                status_detail="Completed",
                status="completed",
                items=json.dumps({"items": [{"name": "Bowl", "qty": 1}]}),
                total_cents=899,
                created_at=datetime.utcnow(),
            ),
        ]
        db.add_all(orders)
        db.commit()
        print("Seeded 2 orders for customer 1")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
