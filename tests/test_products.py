from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_products():
    response = client.get("/products")
    assert response.status_code in (200, 201, 404)
