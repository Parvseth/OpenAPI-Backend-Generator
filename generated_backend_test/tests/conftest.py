import os
import pytest
from fastapi.testclient import TestClient

# Force tests to use an in-memory SQLite database
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app.main import app

@pytest.fixture
def client():
    return TestClient(app)
