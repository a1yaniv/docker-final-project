from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root():
    response = client.get("/api/")
    assert response.status_code == 200
    assert "message" in response.json()

@patch("app.get_db")
def test_get_items(mock_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{"id": 1, "name": "Test"}]
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    response = client.get("/api/items")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Test"

@patch("app.get_db")
def test_add_item(mock_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db.return_value = mock_conn

    response = client.post("/api/items/TestItem")
    assert response.status_code == 200
    assert response.json()["message"] == "Item added"
