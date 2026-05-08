import asyncio
from typing import Any, cast

from sqlalchemy.orm import Session

from app.models import DiningHall, MenuItem
from app.services import menu_cache
from app.services.dining_scraper import HALL_IDS, fetch_menu

_DRINK_KEYWORDS = ("milk", "juice", "water", "coffee", "tea", "lemonade", "smoothie")
_SNACK_PHRASES = ("tossed salad", "fruit salad")
_SNACK_KEYWORDS = (
    "brownie",
    "cookie",
    "muffin top",
    "danish",
    "parfait",
    "oatmeal",
    "cereal",
    "broccoli",
    "carrots",
    "celery",
    "squash",
    "beans",
    "garlic bread",
    "yogurt",
)


def _category_from_item(name: str) -> str:
    low = name.lower()
    if any(k in low for k in _DRINK_KEYWORDS):
        return "drink"
    if any(phrase in low for phrase in _SNACK_PHRASES):
        return "snack"
    if any(k in low for k in _SNACK_KEYWORDS):
        return "snack"
    return "entree"


def _today_str() -> str:
    from datetime import date

    return date.today().strftime("%m/%d/%Y")


async def sync_today_menu_to_db(db: Session) -> None:
    """
    Scrape today's menu for all halls and replace MenuItem rows in the DB.
    DiningHall rows must already exist (created by init_database).
    """
    hall_rows: dict[str, DiningHall] = {
        row.name.lower(): row for row in db.query(DiningHall).all()
    }

    results = await asyncio.gather(
        *[fetch_menu(hall) for hall in HALL_IDS],
        return_exceptions=True,
    )

    menus: dict[str, dict[str, Any]] = {
        hall: result
        for hall, result in zip(HALL_IDS, results)
        if not isinstance(result, BaseException)
    }

    if not menus:
        return

    hall_ids_to_clear = [hall_rows[hall].id for hall in menus if hall in hall_rows]
    if hall_ids_to_clear:
        from app.models import OrderItem

        # Clear order items that reference menu items we're about to replace
        stale_ids = [
            mi.id
            for mi in db.query(MenuItem.id).filter(
                MenuItem.dining_hall_id.in_(hall_ids_to_clear)
            )
        ]
        if stale_ids:
            db.query(OrderItem).filter(OrderItem.menu_item_id.in_(stale_ids)).delete(
                synchronize_session=False
            )
        db.query(MenuItem).filter(
            MenuItem.dining_hall_id.in_(hall_ids_to_clear)
        ).delete(synchronize_session=False)

    today = _today_str()
    new_items: list[MenuItem] = []

    for hall, meals in menus.items():
        dh = hall_rows.get(hall)
        if not dh:
            continue

        # name → MenuItem so we can append meal periods for duplicates
        seen: dict[str, MenuItem] = {}

        for meal_name, stations in meals.items():
            for station, station_items in stations.items():
                meal_name = str(meal_name)
                station = str(station)
                # Stations named "Breakfast *" are breakfast items even when
                # the API nests them under the "lunch" meal key.
                effective_meal = (
                    "breakfast" if "breakfast" in station.lower() else meal_name
                )
                for item in cast(list[dict[str, Any]], station_items):
                    name = item.get("name", "")
                    if not name:
                        continue
                    diets: list[str] = item.get("diets", [])
                    key = name.lower()
                    if key in seen:
                        mi = seen[key]
                        if effective_meal not in mi.meal_type:
                            mi.meal_type = mi.meal_type + [effective_meal]
                        continue

                    mi = MenuItem(
                        name=name,
                        meal_type=[effective_meal],
                        diets=diets,
                        category=_category_from_item(name),
                        price=13.50,
                        dining_hall_id=dh.id,
                    )
                    seen[key] = mi
                    new_items.append(mi)

        menu_cache.set(hall, today, meals)

    db.add_all(new_items)
    db.commit()
