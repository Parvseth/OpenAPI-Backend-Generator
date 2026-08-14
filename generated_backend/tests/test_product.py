import pytest
from fastapi.testclient import TestClient

def test_list_products(client: TestClient):
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product_not_found(client: TestClient):
    response = client.get("/api/v1/products/999999")
    assert response.status_code == 404
