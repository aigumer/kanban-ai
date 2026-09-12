"""In-memory mock database — drop-in replacement for a real DB later."""

from __future__ import annotations

from datetime import datetime, timezone

from app.schemas import CardRead, ColumnRead, BoardRead

now = lambda: datetime.now(timezone.utc)

# --- seed data ---------------------------------------------------------------

_boards: list[dict] = [
    {"id": 1, "name": "My Board", "created_at": now().isoformat()},
]

_columns: list[dict] = [
    {"id": 1, "board_id": 1, "name": "To Do", "position": 0},
    {"id": 2, "board_id": 1, "name": "In Progress", "position": 1},
    {"id": 3, "board_id": 1, "name": "Done", "position": 2},
]

_cards: list[dict] = []
_next_card_id = 1


def _next_id() -> int:
    global _next_card_id
    id_ = _next_card_id
    _next_card_id += 1
    return id_


# --- board -------------------------------------------------------------------

def get_board() -> dict | None:
    return _boards[0] if _boards else None


# --- columns -----------------------------------------------------------------

def get_columns() -> list[dict]:
    return sorted(_columns, key=lambda c: c["position"])


# --- cards -------------------------------------------------------------------

def get_cards(column_id: int | None = None) -> list[dict]:
    cards = _cards if column_id is None else [c for c in _cards if c["column_id"] == column_id]
    return sorted(cards, key=lambda c: c["position"])


def get_card(card_id: int) -> dict | None:
    return next((c for c in _cards if c["id"] == card_id), None)


def create_card(column_id: int, title: str, description: str | None = None) -> dict:
    position = len([c for c in _cards if c["column_id"] == column_id])
    ts = now().isoformat()
    card = {
        "id": _next_id(),
        "column_id": column_id,
        "title": title,
        "description": description,
        "position": position,
        "timer_seconds": 0,
        "timer_running": False,
        "timer_started_at": None,
        "created_at": ts,
        "updated_at": ts,
    }
    _cards.append(card)
    return card


def update_card(card_id: int, **fields) -> dict | None:
    card = get_card(card_id)
    if card is None:
        return None
    for k, v in fields.items():
        if v is not None:
            card[k] = v
    card["updated_at"] = now().isoformat()
    return card


def delete_card(card_id: int) -> bool:
    idx = next((i for i, c in enumerate(_cards) if c["id"] == card_id), None)
    if idx is None:
        return False
    _cards.pop(idx)
    return True


def start_timer(card_id: int) -> dict | None:
    card = get_card(card_id)
    if card is None:
        return None
    card["timer_running"] = True
    card["timer_started_at"] = now().isoformat()
    card["updated_at"] = now().isoformat()
    return card


def stop_timer(card_id: int) -> dict | None:
    card = get_card(card_id)
    if card is None:
        return None
    if card["timer_running"] and card["timer_started_at"]:
        started = datetime.fromisoformat(card["timer_started_at"])
        elapsed = int((now() - started).total_seconds())
        card["timer_seconds"] += elapsed
    card["timer_running"] = False
    card["timer_started_at"] = None
    card["updated_at"] = now().isoformat()
    return card


def reorder_cards(column_id: int, card_ids: list[int]) -> None:
    """Set positions 0..n for the given cards in column."""
    cards_in_col = [c for c in _cards if c["column_id"] == column_id]
    for pos, cid in enumerate(card_ids):
        card = next((c for c in cards_in_col if c["id"] == cid), None)
        if card:
            card["position"] = pos


def reset() -> None:
    """Reset DB to seed state (useful for tests)."""
    global _cards, _next_card_id
    _cards.clear()
    _next_card_id = 1
