from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert "Chess Club" in data


def test_signup_and_remove():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Ensure not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup -> 400
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 400

    # Remove participant
    r = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert r.status_code == 200
    assert email not in activities[activity]["participants"]
