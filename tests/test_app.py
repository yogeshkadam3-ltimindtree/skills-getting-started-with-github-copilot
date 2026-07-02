from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_from_activity():
    email = "teststudent@example.com"

    signup_response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )
    assert signup_response.status_code == 200

    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_not_found():
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "missingstudent@example.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
