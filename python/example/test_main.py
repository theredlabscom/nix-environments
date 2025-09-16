from sqlmodel import Session, SQLModel, create_engine
from fastapi.testclient import TestClient

from main import app, Friend, create_db_and_tables, engine

def test_create_friend():
    with TestClient(app) as client:
        response = client.post(
            "/friends/", json={"name": "Alice", "city": "New York", "country": "USA", "phone": "111-222-3333"}
        )
        data = response.json()
        assert response.status_code == 200
        assert data["name"] == "Alice"
        assert data["city"] == "New York"
        assert data["country"] == "USA"
        assert data["phone"] == "111-222-3333"
        assert data["id"] is not None

def test_read_friends():
    with TestClient(app) as client:
        response = client.get("/friends/")
        data = response.json()
        assert response.status_code == 200
        assert isinstance(data, list)

def test_read_friend():
    with TestClient(app) as client:
        # Create a friend first
        post_response = client.post(
            "/friends/", json={"name": "Bob", "city": "London", "country": "UK", "phone": "444-555-6666"}
        )
        friend_id = post_response.json()["id"]

        response = client.get(f"/friends/{friend_id}")
        data = response.json()
        assert response.status_code == 200
        assert data["name"] == "Bob"

def test_update_friend():
    with TestClient(app) as client:
        # Create a friend first
        post_response = client.post(
            "/friends/", json={"name": "Charlie", "city": "Paris", "country": "France", "phone": "777-888-9999"}
        )
        friend_id = post_response.json()["id"]

        response = client.put(
            f"/friends/{friend_id}", json={"name": "Charles", "city": "Paris", "country": "France", "phone": "777-888-9999"}
        )
        data = response.json()
        assert response.status_code == 200
        assert data["name"] == "Charles"

def test_delete_friend():
    with TestClient(app) as client:
        # Create a friend first
        post_response = client.post(
            "/friends/", json={"name": "David", "city": "Berlin", "country": "Germany", "phone": "000-111-2222"}
        )
        friend_id = post_response.json()["id"]

        response = client.delete(f"/friends/{friend_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Friend deleted successfully"}

        # Verify deletion
        get_response = client.get(f"/friends/{friend_id}")
        assert get_response.status_code == 404

def test_read_nonexistent_friend():
    with TestClient(app) as client:
        response = client.get("/friends/99999")  # Assuming 99999 doesn't exist
        assert response.status_code == 404
        assert response.json() == {"detail": "Friend not found"}

def test_update_nonexistent_friend():
    with TestClient(app) as client:
        response = client.put(
            "/friends/99999", json={"name": "NonExistent", "city": "Nowhere", "country": "None", "phone": "000-000-0000"}
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Friend not found"}

def test_delete_nonexistent_friend():
    with TestClient(app) as client:
        response = client.delete("/friends/99999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Friend not found"}
