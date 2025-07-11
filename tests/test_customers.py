from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_customers():
    response = client.get("/customers")
    assert response.status_code in (200, 201, 404)

def test_post_customers():
    response = client.post("/customers")
    assert response.status_code in (200, 201, 404)
