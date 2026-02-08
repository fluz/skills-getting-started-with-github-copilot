from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_signup_for_activity():
    response = client.post("/activities/Basketball Team/signup", params={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up test@example.com for Basketball Team"


def test_unregister_participant():
    # First, sign up a participant
    client.post("/activities/Basketball Team/signup", params={"email": "test@example.com"})

    # Then, unregister the participant
    response = client.delete("/activities/Basketball Team/unregister", params={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered test@example.com from Basketball Team"


def test_unregister_nonexistent_participant():
    response = client.delete("/activities/Basketball Team/unregister", params={"email": "nonexistent@example.com"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"