import pytest
from fastapi.testclient import TestClient


class TestDeleteParticipantEndpoint:
    """Test cases for removing participants from activities"""

    def test_delete_participant_success(self, client: TestClient):
        # Arrange
        activity_name = "Chess Club"
        email = "daniel@mergington.edu"  # Already exists
        expected_status_code = 200

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status_code
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_delete_from_nonexistent_activity(self, client: TestClient):
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@example.com"
        expected_status_code = 404

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status_code
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_delete_nonexistent_participant(self, client: TestClient):
        # Arrange
        activity_name = "Chess Club"
        email = "nonexistent@example.com"
        expected_status_code = 400

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status_code
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()

    def test_delete_with_url_encoding(self, client: TestClient):
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"
        expected_status_code = 200

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == expected_status_code
        data = response.json()
        assert "message" in data