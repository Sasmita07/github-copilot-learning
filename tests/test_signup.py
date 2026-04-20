import pytest
from fastapi.testclient import TestClient


class TestSignupEndpoint:
    """Test cases for activity signup functionality"""

    def test_signup_success(self, client: TestClient):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@example.com"
        expected_status_code = 200

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status_code
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_nonexistent_activity(self, client: TestClient):
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@example.com"
        expected_status_code = 404

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status_code
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_duplicate_participant(self, client: TestClient):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        expected_status_code = 400

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status_code
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_with_url_encoding(self, client: TestClient):
        # Arrange
        activity_name = "Programming Class"
        email = "test+user@example.com"
        expected_status_code = 200

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == expected_status_code
        data = response.json()
        assert "message" in data