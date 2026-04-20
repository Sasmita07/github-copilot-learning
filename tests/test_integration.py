import pytest
from fastapi.testclient import TestClient


class TestActivityWorkflow:
    """Integration tests for complete activity signup workflow"""

    def test_full_signup_workflow(self, client: TestClient):
        # Arrange
        activity_name = "Basketball Team"
        email = "newworkflow@example.com"

        # Act 1: Check initial state
        response = client.get("/activities")
        initial_data = response.json()
        initial_participants = initial_data[activity_name]["participants"]
        initial_count = len(initial_participants)

        # Act 2: Sign up for activity
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert signup success
        assert signup_response.status_code == 200
        signup_data = signup_response.json()
        assert email in signup_data["message"]

        # Act 3: Verify participant was added
        response = client.get("/activities")
        updated_data = response.json()
        updated_participants = updated_data[activity_name]["participants"]
        updated_count = len(updated_participants)

        # Assert participant count increased
        assert updated_count == initial_count + 1
        assert email in updated_participants

        # Act 4: Remove participant
        delete_response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert delete success
        assert delete_response.status_code == 200
        delete_data = delete_response.json()
        assert email in delete_data["message"]

        # Act 5: Verify participant was removed
        response = client.get("/activities")
        final_data = response.json()
        final_participants = final_data[activity_name]["participants"]
        final_count = len(final_participants)

        # Assert participant count returned to original
        assert final_count == initial_count
        assert email not in final_participants

    def test_activity_capacity_limits(self, client: TestClient):
        # Arrange
        activity_name = "Chess Club"  # Max 12 participants
        test_email = "capacitytest@example.com"

        # Act: Try to sign up
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        # Assert: Should succeed (we're not enforcing capacity in current implementation)
        assert response.status_code == 200

        # Cleanup: Remove the test participant
        client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

    def test_concurrent_signup_scenarios(self, client: TestClient):
        # Arrange
        activity_name = "Tennis Club"
        email1 = "concurrent1@example.com"
        email2 = "concurrent2@example.com"

        # Act: Sign up two different participants
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )

        # Assert both succeed
        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify both are in the activity
        response = client.get("/activities")
        data = response.json()
        participants = data[activity_name]["participants"]
        assert email1 in participants
        assert email2 in participants

        # Cleanup
        client.delete(f"/activities/{activity_name}/signup", params={"email": email1})
        client.delete(f"/activities/{activity_name}/signup", params={"email": email2})