from __future__ import annotations


# ── Board ────────────────────────────────────────────────────────────────────

class TestBoard:
    def test_get_board(self, client):
        r = client.get("/api/board")
        assert r.status_code == 200
        body = r.json()
        assert body["name"] == "My Board"
        assert "id" in body
        assert "created_at" in body


# ── Columns ──────────────────────────────────────────────────────────────────

class TestColumns:
    def test_list_columns(self, client):
        r = client.get("/api/columns")
        assert r.status_code == 200
        cols = r.json()
        assert len(cols) == 3
        names = [c["name"] for c in cols]
        assert names == ["To Do", "In Progress", "Done"]

    def test_columns_have_positions(self, client):
        r = client.get("/api/columns")
        positions = [c["position"] for c in r.json()]
        assert positions == [0, 1, 2]

    def test_columns_belong_to_board(self, client):
        r = client.get("/api/columns")
        board_id = client.get("/api/board").json()["id"]
        for col in r.json():
            assert col["board_id"] == board_id


# ── Cards CRUD ───────────────────────────────────────────────────────────────

class TestCardsCRUD:
    def test_list_cards_empty(self, client):
        r = client.get("/api/cards")
        assert r.status_code == 200
        assert r.json() == []

    def test_list_cards_by_column(self, client):
        client.post("/api/cards", json={"column_id": 1, "title": "A"})
        client.post("/api/cards", json={"column_id": 2, "title": "B"})
        r = client.get("/api/cards", params={"column_id": 1})
        assert len(r.json()) == 1
        assert r.json()[0]["title"] == "A"

    def test_list_all_cards(self, client):
        client.post("/api/cards", json={"column_id": 1, "title": "A"})
        client.post("/api/cards", json={"column_id": 2, "title": "B"})
        r = client.get("/api/cards")
        assert len(r.json()) == 2

    def test_create_card(self, client):
        r = client.post("/api/cards", json={"column_id": 1, "title": "Test"})
        assert r.status_code == 201
        body = r.json()
        assert body["title"] == "Test"
        assert body["column_id"] == 1
        assert body["position"] == 0
        assert body["timer_seconds"] == 0
        assert body["timer_running"] is False
        assert body["timer_started_at"] is None

    def test_create_card_with_description(self, client):
        r = client.post(
            "/api/cards",
            json={"column_id": 1, "title": "X", "description": "desc"},
        )
        assert r.json()["description"] == "desc"

    def test_create_card_without_description(self, client):
        r = client.post("/api/cards", json={"column_id": 1, "title": "X"})
        assert r.json()["description"] is None

    def test_create_card_position_increments(self, client):
        client.post("/api/cards", json={"column_id": 1, "title": "A"})
        r = client.post("/api/cards", json={"column_id": 1, "title": "B"})
        assert r.json()["position"] == 1

    def test_create_card_positions_independent_per_column(self, client):
        client.post("/api/cards", json={"column_id": 1, "title": "A"})
        r = client.post("/api/cards", json={"column_id": 2, "title": "B"})
        assert r.json()["position"] == 0

    def test_create_card_has_timestamps(self, client):
        r = client.post("/api/cards", json={"column_id": 1, "title": "X"})
        body = r.json()
        assert body["created_at"] is not None
        assert body["updated_at"] is not None

    def test_update_card_title(self, client):
        c = client.post("/api/cards", json={"column_id": 1, "title": "Old"}).json()
        r = client.patch(f"/api/cards/{c['id']}", json={"title": "New"})
        assert r.status_code == 200
        assert r.json()["title"] == "New"

    def test_update_card_description(self, client):
        c = client.post("/api/cards", json={"column_id": 1, "title": "X"}).json()
        r = client.patch(f"/api/cards/{c['id']}", json={"description": "hello"})
        assert r.json()["description"] == "hello"

    def test_update_card_clear_description(self, client):
        c = client.post(
            "/api/cards", json={"column_id": 1, "title": "X", "description": "d"}
        ).json()
        r = client.patch(f"/api/cards/{c['id']}", json={"description": None})
        assert r.json()["description"] is None

    def test_update_card_position(self, client):
        c = client.post("/api/cards", json={"column_id": 1, "title": "X"}).json()
        r = client.patch(f"/api/cards/{c['id']}", json={"position": 5})
        assert r.json()["position"] == 5

    def test_update_card_column(self, client):
        c = client.post("/api/cards", json={"column_id": 1, "title": "X"}).json()
        r = client.patch(f"/api/cards/{c['id']}", json={"column_id": 2})
        assert r.json()["column_id"] == 2

    def test_update_card_touches_updated_at(self, client):
        c = client.post("/api/cards", json={"column_id": 1, "title": "X"}).json()
        old_updated = c["updated_at"]
        r = client.patch(f"/api/cards/{c['id']}", json={"title": "Y"})
        assert r.json()["updated_at"] != old_updated

    def test_update_nonexistent_card(self, client):
        r = client.patch("/api/cards/999", json={"title": "X"})
        assert r.status_code == 404

    def test_delete_card(self, client):
        c = client.post("/api/cards", json={"column_id": 1, "title": "X"}).json()
        r = client.delete(f"/api/cards/{c['id']}")
        assert r.status_code == 204
        assert client.get("/api/cards").json() == []

    def test_delete_nonexistent_card(self, client):
        r = client.delete("/api/cards/999")
        assert r.status_code == 404

    def test_delete_does_not_affect_other_columns(self, client):
        c1 = client.post("/api/cards", json={"column_id": 1, "title": "A"}).json()
        client.post("/api/cards", json={"column_id": 2, "title": "B"})
        client.delete(f"/api/cards/{c1['id']}")
        r = client.get("/api/cards", params={"column_id": 2})
        assert len(r.json()) == 1


# ── Timer ────────────────────────────────────────────────────────────────────

class TestTimer:
    def test_start_timer(self, client):
        c = client.post("/api/cards", json={"column_id": 1, "title": "T"}).json()
        r = client.post(f"/api/cards/{c['id']}/timer/start")
        assert r.status_code == 200
        body = r.json()
        assert body["timer_running"] is True
        assert body["timer_started_at"] is not None

    def test_stop_timer(self, client):
        c = client.post("/api/cards", json={"column_id": 1, "title": "T"}).json()
        client.post(f"/api/cards/{c['id']}/timer/start")
        r = client.post(f"/api/cards/{c['id']}/timer/stop")
        body = r.json()
        assert body["timer_running"] is False
        assert body["timer_started_at"] is None
        assert body["timer_seconds"] >= 0

    def test_stop_timer_accumulates(self, client):
        c = client.post("/api/cards", json={"column_id": 1, "title": "T"}).json()
        client.post(f"/api/cards/{c['id']}/timer/start")
        client.post(f"/api/cards/{c['id']}/timer/stop")
        first = client.get("/api/cards").json()[0]["timer_seconds"]
        client.post(f"/api/cards/{c['id']}/timer/start")
        client.post(f"/api/cards/{c['id']}/timer/stop")
        second = client.get("/api/cards").json()[0]["timer_seconds"]
        assert second >= first

    def test_stop_without_start_does_not_change_time(self, client):
        c = client.post("/api/cards", json={"column_id": 1, "title": "T"}).json()
        before = client.get("/api/cards").json()[0]["timer_seconds"]
        client.post(f"/api/cards/{c['id']}/timer/stop")
        after = client.get("/api/cards").json()[0]["timer_seconds"]
        assert after == before

    def test_start_nonexistent_card(self, client):
        r = client.post("/api/cards/999/timer/start")
        assert r.status_code == 404

    def test_stop_nonexistent_card(self, client):
        r = client.post("/api/cards/999/timer/stop")
        assert r.status_code == 404

    def test_start_updates_updated_at(self, client):
        c = client.post("/api/cards", json={"column_id": 1, "title": "T"}).json()
        old_updated = c["updated_at"]
        r = client.post(f"/api/cards/{c['id']}/timer/start")
        assert r.json()["updated_at"] != old_updated

    def test_stop_updates_updated_at(self, client):
        c = client.post("/api/cards", json={"column_id": 1, "title": "T"}).json()
        client.post(f"/api/cards/{c['id']}/timer/start")
        old_updated = client.get("/api/cards").json()[0]["updated_at"]
        r = client.post(f"/api/cards/{c['id']}/timer/stop")
        assert r.json()["updated_at"] != old_updated
