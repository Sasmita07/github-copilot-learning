import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """FastAPI test client fixture"""
    return TestClient(app)


@pytest.fixture
def sample_activity():
    """Sample activity data for testing"""
    return {
        "name": "Test Activity",
        "description": "A test activity",
        "schedule": "Test schedule",
        "max_participants": 10,
        "participants": []
    }


@pytest.fixture
def sample_email():
    """Sample email for testing"""
    return "test@example.com"