import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def client():
    app_module.activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]

    with TestClient(app_module.app) as test_client:
        yield test_client


def test_unregister_participant_from_activity(client):
    # Arrange
    email = "teststudent@example.com"
    activity_name = "Chess Club"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    unregister_response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_missing_participant_returns_not_found(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missingstudent@example.com"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
