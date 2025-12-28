from urllib.parse import quote
import json

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect some known activity keys
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Basketball Team"
    email = "alice@example.com"

    # Ensure not present initially
    resp = client.get("/activities")
    assert resp.status_code == 200
    before = resp.json()
    assert email not in before[activity]["participants"]

    # Sign up
    signup_url = f"/activities/{quote(activity)}/signup?email={quote(email)}"
    resp = client.post(signup_url)
    assert resp.status_code == 200
    body = resp.json()
    assert "Signed up" in body.get("message", "")

    # Confirm participant present
    resp = client.get("/activities")
    assert resp.status_code == 200
    after = resp.json()
    assert email in after[activity]["participants"]

    # Unregister
    unreg_url = f"/activities/{quote(activity)}/unregister?email={quote(email)}"
    resp = client.delete(unreg_url)
    assert resp.status_code == 200
    body = resp.json()
    assert "Unregistered" in body.get("message", "")

    # Confirm removed
    resp = client.get("/activities")
    assert resp.status_code == 200
    final = resp.json()
    assert email not in final[activity]["participants"]
