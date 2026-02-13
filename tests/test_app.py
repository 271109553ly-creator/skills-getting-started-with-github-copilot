import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, get_initial_activities

@pytest.fixture(autouse=True)
def reset_activities():
    app.state.activities = get_initial_activities()

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data

def test_signup_and_unregister():
    # signup
    response = client.post("/activities/Basketball/signup?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    # duplicate signup
    response = client.post("/activities/Basketball/signup?email=tester@mergington.edu")
    assert response.status_code == 400
    # unregister
    response = client.delete("/activities/Basketball/unregister?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    # unregister again
    response = client.delete("/activities/Basketball/unregister?email=tester@mergington.edu")
    assert response.status_code == 404

def test_signup_activity_not_found():
    response = client.post("/activities/NotExist/signup?email=abc@mergington.edu")
    assert response.status_code == 404

def test_unregister_activity_not_found():
    response = client.delete("/activities/NotExist/unregister?email=abc@mergington.edu")
    assert response.status_code == 404
