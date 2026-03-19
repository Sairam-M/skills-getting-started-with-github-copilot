import pytest
import copy
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    """Test client fixture for FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to original state after each test."""
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)