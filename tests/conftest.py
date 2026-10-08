import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers.recipes import reset_store


@pytest.fixture
def client():
    reset_store()
    return TestClient(app)
