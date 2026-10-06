from uuid import uuid4

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = f"{uuid4()}@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    delete_response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert delete_response.status_code == 200
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_participant_returns_404_for_missing_activity():
    # Arrange
    path = "/activities/Unknown Activity/participants"
    params = {"email": "test@example.com"}

    # Act
    response = client.delete(path, params=params)

    # Assert
    assert response.status_code == 404
