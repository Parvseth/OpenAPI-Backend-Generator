from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_customers_customer_id():
    response = client.get("/customers/{customer_id}")
    assert response.status_code in (200, 201, 404)
