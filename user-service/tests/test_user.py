import pytest
from fastapi.testclient import TestClient
import app as app_module

client = TestClient(app_module.app)

User = app_module.User


@pytest.fixture(autouse=True)
def reset_users():
    app_module.users.clear()
    app_module.users.extend([
        User(id=1, name="Alice"),
        User(id=2, name="Bob"),
        User(id=3, name="Charlie")
    ])


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_post_user():
    new_user = {"name": "Ansar"}
    response = client.post("/users", json=new_user)
    assert response.status_code == 201
    assert response.json()["name"] == "Ansar"


def test_Update_user():
    updated_user = {"name": "Updated Name"}
    response = client.put("/users/1", json=updated_user)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"


def test_update_user_not_found():
    updated_user = {"name": "Updated Name"}
    response = client.put("/users/999", json=updated_user)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"message": "user deleted successfully"}
