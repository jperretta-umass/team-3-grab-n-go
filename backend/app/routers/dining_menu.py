from datetime import date
from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.services import dining_scraper, menu_cache

router = APIRouter(prefix="/api/dining-menu", tags=["dining-menu"])


@router.get("")
async def get_dining_menu(
    hall: str = Query(..., description="worcester | franklin | hampshire | berkshire"),
    menu_date: str = Query(
        None,
        alias="date",
        description="MM/DD/YYYY — defaults to today",
    ),
) -> dict[str, Any]:
    if hall.lower() not in dining_scraper.HALL_IDS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown hall '{hall}'. Valid options: {list(dining_scraper.HALL_IDS)}",
        )

    date_str = menu_date or date.today().strftime("%m/%d/%Y")

    cached = menu_cache.get(hall, date_str)
    if cached is not None:
        return {"hall": hall, "date": date_str, "meals": cached}

    try:
        meals = await dining_scraper.fetch_menu(hall, date_str)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Failed to fetch menu: {exc}")

    menu_cache.set(hall, date_str, meals)
    return {"hall": hall, "date": date_str, "meals": meals}
