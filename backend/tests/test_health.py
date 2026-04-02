from fastapi.testclient import TestClient
from app.main import app


def test_health():
    """
    Basic smoke test for backend availability.

    This verifies that the application starts and a simple route responds
    with the expected payload.

    IMPORTANT FOR FUTURE DATABASE IMPLEMENTATION:
    If the health endpoint path or response changes, update this test.
    """
    c = TestClient(app)
    assert c.get("/health").json() == {"message": "Hello"}