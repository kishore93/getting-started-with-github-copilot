import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    # Store initial state
    initial_activities = copy.deepcopy(activities)
    yield
    # Reset to initial state after each test
    activities.clear()
    activities.update(initial_activities)