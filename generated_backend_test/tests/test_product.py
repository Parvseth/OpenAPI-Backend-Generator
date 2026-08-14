import pytest
from fastapi.testclient import TestClient

def test_create_product(client: TestClient):
    payload = {







    }
    response = client.post("/api/v1/products/", json=payload)
    assert response.status_code in (200, 201), response.text

def test_list_products(client: TestClient):
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product_not_found(client: TestClient):
    response = client.get("/api/v1/products/999999")
    assert response.status_code == 404
