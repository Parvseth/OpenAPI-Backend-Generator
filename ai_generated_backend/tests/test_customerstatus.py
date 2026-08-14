import pytest
from fastapi.testclient import TestClient

def test_list_customer_statuss(client: TestClient):
    response = client.get("/api/v1/customer_statuss/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_customerstatus_not_found(client: TestClient):
    response = client.get("/api/v1/customer_statuss/999999")
    assert response.status_code == 404
