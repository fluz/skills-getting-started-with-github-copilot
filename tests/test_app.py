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


def test_signup_with_invalid_email():
    """Test that signup rejects invalid email formats"""
    # Test with XSS attempt
    response = client.post("/activities/Basketball Team/signup", params={"email": "<script>alert('xss')</script>"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email format"
    
    # Test with incomplete email
    response = client.post("/activities/Basketball Team/signup", params={"email": "notanemail"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email format"
    
    # Test with HTML injection attempt
    response = client.post("/activities/Basketball Team/signup", params={"email": "<img src=x onerror=alert(1)>@test.com"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email format"
    
    # Test with extremely long email
    long_email = "a" * 300 + "@test.com"
    response = client.post("/activities/Basketball Team/signup", params={"email": long_email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email format"
    
    # Test with consecutive dots (invalid per RFC 5322)
    response = client.post("/activities/Basketball Team/signup", params={"email": "user..name@example.com"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email format"
    
    # Test with leading dot
    response = client.post("/activities/Basketball Team/signup", params={"email": ".user@example.com"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email format"
    
    # Test with trailing dot in local part
    response = client.post("/activities/Basketball Team/signup", params={"email": "user.@example.com"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email format"


def test_unregister_with_invalid_email():
    """Test that unregister rejects invalid email formats"""
    response = client.delete("/activities/Basketball Team/unregister", params={"email": "<script>alert('xss')</script>"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email format"