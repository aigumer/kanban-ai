import pytest
from fastapi.testclient import TestClient

from app import db
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_db():
    """Reset mock DB before every test."""
    db.reset()
    yield


# ── Board ────────────────────────────────────────────────────────────────────

class TestBoard:
    def test_get_board(self):
        r = client.get("/api/board")
        assert r.status_code == 200
        body = r.json()
        assert body["name"] == "My Board"
        assert "id" in body
        assert "created_at" in body


# ── Columns ──────────────────────────────────────────────────────────────────

class TestColumns:
    def test_list_columns(self):
        r = client.get("/api/columns")
        assert r.status_code == 200
        cols = r.json()
        assert len(cols) == 3
        names = [c["name"] for c in cols]
        assert names == ["To Do", "In Progress", "Done"]

    def test_columns_have_positions(self):
        r = client.get("/api/columns")
        positions = [c["position"] for c in r.json()]
        assert positions == [0, 1, 2]


# ── Cards CRUD ───────────────────────────────────────────────────────────────

class TestCardsCRUD:
    def test_list_cards_empty(self):
        r = client.get("/api/cards")
        assert r.status_code == 200
        assert r.json() == []

    def test_list_cards_by_column(self):
        client.post("/api/cards", json={"column_id": 1, "title": "A"})
        client.post("/api/cards", json={"column_id": 2, "title": "B"})
        r = client.get("/api/cards", params={"column_id": 1})
        assert len(r.json()) == 1
        assert r.json()[0]["title"] == "A"

    def test_create_card(self):
        r = client.post("/api/cards", json={"column_id": 1, "title": "Test"})
        assert r.status_code == 201
        body = r.json()
        assert body["title"] == "Test"
        assert body["column_id"] == 1
        assert body["position"] == 0
        assert body["timer_seconds"] == 0
        assert body["timer_running"] is False

    def test_create_card_with_description(self):
        r = client.post(
            "/api/cards",
            json={"column_id": 1, "title": "X", "description": "desc"},
        )
        assert r.json()["description"] == "desc"

    def test_create_card_position_increments(self):
        client.post("/api/cards", json={"column_id": 1, "title": "A"})
        r = client.post("/api/cards", json={"column_id": 1, "title": "B"})
        assert r.json()["position"] == 1

    def test_update_card_title(self):
        c = client.post("/api/cards", json={"column_id": 1, "title": "Old"}).json()
        r = client.patch(f"/api/cards/{c['id']}", json={"title": "New"})
        assert r.status_code == 200
        assert r.json()["title"] == "New"

    def test_update_card_description(self):
        c = client.post("/api/cards", json={"column_id": 1, "title": "X"}).json()
        r = client.patch(f"/api/cards/{c['id']}", json={"description": "hello"})
        assert r.json()["description"] == "hello"

    def test_update_nonexistent_card(self):
        r = client.patch("/api/cards/999", json={"title": "X"})
        assert r.status_code == 404

    def test_delete_card(self):
        c = client.post("/api/cards", json={"column_id": 1, "title": "X"}).json()
        r = client.delete(f"/api/cards/{c['id']}")
        assert r.status_code == 204
        assert client.get("/api/cards").json() == []

    def test_delete_nonexistent_card(self):
        r = client.delete("/api/cards/999")
        assert r.status_code == 404


# ── Timer ────────────────────────────────────────────────────────────────────

class TestTimer:
    def test_start_timer(self):
        c = client.post("/api/cards", json={"column_id": 1, "title": "T"}).json()
        r = client.post(f"/api/cards/{c['id']}/timer/start")
        assert r.status_code == 200
        body = r.json()
        assert body["timer_running"] is True
        assert body["timer_started_at"] is not None

    def test_stop_timer(self):
        c = client.post("/api/cards", json={"column_id": 1, "title": "T"}).json()
        client.post(f"/api/cards/{c['id']}/timer/start")
        r = client.post(f"/api/cards/{c['id']}/timer/stop")
        body = r.json()
        assert body["timer_running"] is False
        assert body["timer_started_at"] is None
        assert body["timer_seconds"] >= 0

    def test_start_nonexistent_card(self):
        r = client.post("/api/cards/999/timer/start")
        assert r.status_code == 404

    def test_stop_nonexistent_card(self):
        r = client.post("/api/cards/999/timer/stop")
        assert r.status_code == 404
