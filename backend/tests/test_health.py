from fastapi.testclient import TestClient
from app.main import app


def test_root():
    c = TestClient(app)
    assert c.get("/").json() == {"message": "Hello"}
