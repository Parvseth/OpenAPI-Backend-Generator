import pytest
from fastapi.testclient import TestClient

def test_list_order_items(client: TestClient):
    response = client.get("/api/v1/order_items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_orderitem_not_found(client: TestClient):
    response = client.get("/api/v1/order_items/999999")
    assert response.status_code == 404
