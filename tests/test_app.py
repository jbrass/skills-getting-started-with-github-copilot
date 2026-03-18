from fastapi.testclient import TestClient
from src.app import app
import uuid

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Use a unique email for testing
    test_email = f"pytestuser+{uuid.uuid4()}@mergington.edu"
    activity = "Chess Club"

    # Ensure not already registered
    cleanup_response = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert cleanup_response.status_code in (200, 400)
    if cleanup_response.status_code == 200:
        assert f"Removed {test_email}" in cleanup_response.json()["message"]
    else:
        assert "not registered" in cleanup_response.json()["detail"]

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    assert f"Signed up {test_email}" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert response.status_code == 200
    assert f"Removed {test_email}" in response.json()["message"]

    # Unregister again should fail
    response = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
