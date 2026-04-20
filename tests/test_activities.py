import pytest
from fastapi.testclient import TestClient


class TestRootEndpoint:
    """Test cases for the root endpoint"""

    def test_root_redirect(self, client: TestClient):
        # Arrange
        expected_status_code = 307
        expected_location = "/static/index.html"

        # Act - don't follow redirects
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == expected_status_code
        assert response.headers["location"] == expected_location


class TestActivitiesEndpoint:
    """Test cases for the activities endpoint"""

    def test_get_activities_success(self, client: TestClient):
        # Arrange
        expected_status_code = 200

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == expected_status_code
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0  # Should have activities

        # Check structure of first activity
        first_activity = next(iter(data.values()))
        required_keys = ["description", "schedule", "max_participants", "participants"]
        for key in required_keys:
            assert key in first_activity

    def test_get_activities_returns_all_activities(self, client: TestClient):
        # Arrange
        response = client.get("/activities")
        data = response.json()

        # Act - count activities
        activity_count = len(data)

        # Assert
        assert activity_count > 0
        assert isinstance(data, dict)