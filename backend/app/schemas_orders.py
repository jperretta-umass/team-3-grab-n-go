import json
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator


class OrderOut(BaseModel):
    id: int
    customer_id: int
    order_number: int | None = None
    dining_hall: str | None = None
    pickup_estimate: str | None = None
    status_detail: str | None = None
    status: str
    items: dict[str, Any]
    total_cents: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("items", mode="before")
    @classmethod
    def parse_items(cls, value: Any) -> dict[str, Any]:
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            return json.loads(value)
        return {}
