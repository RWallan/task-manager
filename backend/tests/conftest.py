import pytest
from fastapi.testclient import TestClient
from backend.src.app import app


@pytest.fixture
def client():
    return TestClient(app)
