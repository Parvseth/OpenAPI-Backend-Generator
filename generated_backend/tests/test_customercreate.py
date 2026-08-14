import pytest
from fastapi.testclient import TestClient

def test_list_customer_creates(client: TestClient):
    response = client.get("/api/v1/customer_creates/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_customercreate_not_found(client: TestClient):
    response = client.get("/api/v1/customer_creates/999999")
    assert response.status_code == 404
