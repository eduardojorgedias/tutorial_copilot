from uuid import uuid4

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = f"{uuid4()}@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert delete_response.status_code == 200

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_participant_returns_404_for_missing_activity():
    response = client.delete("/activities/Unknown Activity/participants?email=test@example.com")
    assert response.status_code == 404
