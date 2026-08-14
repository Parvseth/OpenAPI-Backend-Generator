import pytest
from fastapi.testclient import TestClient

def test_create_customercreate(client: TestClient):
    payload = {





        "name": "test_string",





        "email": "test_string",



    }
    response = client.post("/api/v1/customer_creates/", json=payload)
    assert response.status_code in (200, 201), response.text

def test_list_customer_creates(client: TestClient):
    response = client.get("/api/v1/customer_creates/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_customercreate_not_found(client: TestClient):
    response = client.get("/api/v1/customer_creates/999999")
    assert response.status_code == 404
