from datetime import date
from typing import Optional

# cache[(hall, date_str)] = parsed meals dict
_cache: dict[tuple[str, str], dict] = {}

# tracks which date the cache was last populated, so it auto-invalidates at midnight
_cache_date: Optional[date] = None


def _maybe_invalidate() -> None:
    global _cache_date
    today = date.today()
    if _cache_date != today:
        _cache.clear()
        _cache_date = today


def get(hall: str, date_str: str) -> Optional[dict]:
    _maybe_invalidate()
    return _cache.get((hall.lower(), date_str))


def set(hall: str, date_str: str, data: dict) -> None:
    _maybe_invalidate()
    _cache[(hall.lower(), date_str)] = data
