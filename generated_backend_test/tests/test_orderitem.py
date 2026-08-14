import pytest
from fastapi.testclient import TestClient

def test_create_orderitem(client: TestClient):
    payload = {





        "product_id": 1,





        "quantity": 1,



    }
    response = client.post("/api/v1/order_items/", json=payload)
    assert response.status_code in (200, 201), response.text

def test_list_order_items(client: TestClient):
    response = client.get("/api/v1/order_items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_orderitem_not_found(client: TestClient):
    response = client.get("/api/v1/order_items/999999")
    assert response.status_code == 404
