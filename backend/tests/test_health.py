from fastapi.testclient import TestClient
from app.main import app


def test_health():
    c = TestClient(app)
    assert c.get("/api/health").json() == {"ok": True}
