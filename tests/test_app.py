from fastapi.testclient import TestClient
from src.app import app, activities
import copy

client = TestClient(app)

# Store the initial state of activities
INITIAL_ACTIVITIES_STATE = {
    "Basketball Team": {
        "description": "Competitive basketball training and games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Swimming Club": {
        "description": "Swimming training and water sports",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Art Studio": {
        "description": "Express creativity through painting and drawing",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Drama Club": {
        "description": "Theater arts and performance training",
        "schedule": "Tuesdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": []
    },
    "Debate Team": {
        "description": "Learn public speaking and argumentation skills",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": []
    },
    "Science Club": {
        "description": "Hands-on experiments and scientific exploration",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities state before each test to avoid test interdependencies"""
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES_STATE))
    yield


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