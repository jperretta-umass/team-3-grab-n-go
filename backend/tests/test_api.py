import pytest
from fastapi.testclient import TestClient

from app.main import app, reset_mock_db


@pytest.fixture()
def client() -> TestClient:
    reset_mock_db()
    return TestClient(app)


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "backend": "healthy"}


def test_root_exposes_implementation_order(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "Grab & Go API"
    assert payload["implementationOrder"] == [
        "Validate request and ids",
        "Run SQL query against schema tables or mock rows",
        "Return JSON payload for the Vue client",
    ]
    assert "Orders" in payload["mockSchemaTables"]


def test_get_cart_returns_mock_payload(client: TestClient) -> None:
    response = client.get("/customer/cart/1")

    assert response.status_code == 200
    payload = response.json()
    assert payload["cartId"] == 1
    assert payload["customerId"] == 101
    assert payload["total"] == 22.75
    assert len(payload["items"]) == 2


def test_add_item_to_cart_updates_mock_state(client: TestClient) -> None:
    response = client.post("/customer/cart/1/item/4")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "Item added to cart"
    assert any(item["itemId"] == 4 for item in payload["cart"]["items"])


def test_patch_cart_updates_quantity(client: TestClient) -> None:
    response = client.patch("/customer/cart/1/item/1", json={"quantity": 3})

    assert response.status_code == 200
    payload = response.json()
    updated_item = next(item for item in payload["cart"]["items"] if item["itemId"] == 1)
    assert updated_item["quantity"] == 3
    assert payload["cart"]["total"] == 49.25


def test_delete_cart_item_removes_it(client: TestClient) -> None:
    response = client.delete("/customer/cart/2")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "Item removed from cart"
    assert all(item["cartItemId"] != 2 for item in payload["cart"]["items"])


def test_get_dining_hall_items_returns_items(client: TestClient) -> None:
    response = client.get("/customer/dininghalls/items/1")

    assert response.status_code == 200
    payload = response.json()
    assert payload["diningHall"]["DhName"] == "Hampshire"
    assert len(payload["items"]) == 3


def test_claim_order_sets_deliverer(client: TestClient) -> None:
    response = client.put("/deliverer/claim/17/order/5001")

    assert response.status_code == 200
    payload = response.json()
    assert payload["order"]["delivererId"] == 17
    assert payload["order"]["status"] == "claimed"


def test_claim_order_conflict_is_reported(client: TestClient) -> None:
    response = client.put("/deliverer/claim/17/order/5002")

    assert response.status_code == 409
    assert "already claimed" in response.json()["detail"]


def test_complete_order_requires_owner(client: TestClient) -> None:
    response = client.post("/deliverer/past-orders/99/order/5002")

    assert response.status_code == 403
    assert "cannot close" in response.json()["detail"]
