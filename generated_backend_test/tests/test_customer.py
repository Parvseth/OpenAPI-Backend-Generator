import pytest
from fastapi.testclient import TestClient

def test_create_customer(client: TestClient):
    payload = {









    }
    response = client.post("/api/v1/customers/", json=payload)
    assert response.status_code in (200, 201), response.text

def test_list_customers(client: TestClient):
    response = client.get("/api/v1/customers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_customer_not_found(client: TestClient):
    response = client.get("/api/v1/customers/999999")
    assert response.status_code == 404
