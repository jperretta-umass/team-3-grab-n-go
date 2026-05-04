from bs4 import BeautifulSoup
import httpx

BASE_URL = "https://umassdining.com/foodpro-menu-ajax"

HALL_IDS: dict[str, int] = {
    "worcester": 10667,
    "franklin": 10716,
    "hampshire": 10715,
    "berkshire": 10666,
}

_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://umassdining.com/",
}


async def fetch_menu(hall: str, date_str: str | None = None) -> dict:
    """
    Returns parsed menu for a hall on a given date.
    date_str must be MM/DD/YYYY. Defaults to today if omitted.
    Raises ValueError for unknown hall, httpx.HTTPError on network failure.
    """
    if date_str is None:
        from datetime import date
        date_str = date.today().strftime("%m/%d/%Y")

    tid = HALL_IDS.get(hall.lower())
    if tid is None:
        raise ValueError(f"Unknown hall '{hall}'. Valid options: {list(HALL_IDS)}")

    async with httpx.AsyncClient(headers=_HEADERS, timeout=20) as client:
        resp = await client.get(BASE_URL, params={"tid": tid, "date": date_str})
        resp.raise_for_status()
        raw = resp.json()

    return _parse(raw)


def _parse(raw: dict) -> dict:
    meals: dict[str, dict[str, list[str]]] = {}

    for meal, stations in raw.items():
        if not isinstance(stations, dict):
            continue
        parsed_stations: dict[str, list[str]] = {}
        for station, html in stations.items():
            if not isinstance(html, str):
                continue
            soup = BeautifulSoup(html, "html.parser")
            items = [
                li.get_text(" ", strip=True)
                for li in soup.find_all("li")
                if li.get_text(" ", strip=True)
            ]
            if items:
                parsed_stations[station] = items
        if parsed_stations:
            meals[meal] = parsed_stations

    return meals
