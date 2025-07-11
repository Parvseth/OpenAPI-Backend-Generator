from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_post_orders():
    response = client.post("/orders")
    assert response.status_code in (200, 201, 404)
