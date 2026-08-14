import pytest
from fastapi.testclient import TestClient

def test_create_ordercreate(client: TestClient):
    payload = {





        "customer_id": 1,





        "items": "test",



    }
    response = client.post("/api/v1/order_creates/", json=payload)
    assert response.status_code in (200, 201), response.text

def test_list_order_creates(client: TestClient):
    response = client.get("/api/v1/order_creates/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_ordercreate_not_found(client: TestClient):
    response = client.get("/api/v1/order_creates/999999")
    assert response.status_code == 404
