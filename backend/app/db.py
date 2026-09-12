"""SQLAlchemy-backed database layer.

All functions require an explicit Session — routes inject it via Depends(get_db).
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Board, Card, Column

_default_columns = ["To Do", "In Progress", "Done"]


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _ensure_aware(dt: datetime | None) -> datetime | None:
    """SQLite returns naive datetimes; force UTC awareness for arithmetic."""
    if dt is not None and dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def seed(session: Session) -> None:
    """Create default board + columns if the DB is empty."""
    if session.execute(select(Board)).scalar() is not None:
        return
    board = Board(name="My Board")
    session.add(board)
    session.flush()
    for i, name in enumerate(_default_columns):
        session.add(Column(board_id=board.id, name=name, position=i))
    session.commit()


def _card_to_dict(card: Card) -> dict:
    return {
        "id": card.id,
        "column_id": card.column_id,
        "title": card.title,
        "description": card.description,
        "position": card.position,
        "timer_seconds": card.timer_seconds,
        "timer_running": card.timer_running,
        "timer_started_at": card.timer_started_at,
        "created_at": card.created_at,
        "updated_at": card.updated_at,
    }


# --- board -------------------------------------------------------------------

def get_board(session: Session) -> dict | None:
    seed(session)
    board = session.execute(select(Board)).scalar_one()
    return {"id": board.id, "name": board.name, "created_at": board.created_at}


# --- columns -----------------------------------------------------------------

def get_columns(session: Session) -> list[dict]:
    seed(session)
    cols = session.execute(select(Column).order_by(Column.position)).scalars().all()
    return [{"id": c.id, "board_id": c.board_id, "name": c.name, "position": c.position} for c in cols]


# --- cards -------------------------------------------------------------------

def get_cards(session: Session, column_id: int | None = None) -> list[dict]:
    stmt = select(Card)
    if column_id is not None:
        stmt = stmt.where(Card.column_id == column_id)
    stmt = stmt.order_by(Card.position)
    cards = session.execute(stmt).scalars().all()
    return [_card_to_dict(c) for c in cards]


def get_card(session: Session, card_id: int) -> dict | None:
    card = session.get(Card, card_id)
    return _card_to_dict(card) if card else None


def create_card(session: Session, column_id: int, title: str, description: str | None = None) -> dict:
    count = session.scalar(select(func.count()).where(Card.column_id == column_id))
    ts = _utcnow()
    card = Card(
        column_id=column_id,
        title=title,
        description=description,
        position=count,
        timer_seconds=0,
        timer_running=False,
        timer_started_at=None,
        created_at=ts,
        updated_at=ts,
    )
    session.add(card)
    session.commit()
    session.refresh(card)
    return _card_to_dict(card)


def update_card(session: Session, card_id: int, **fields) -> dict | None:
    card = session.get(Card, card_id)
    if card is None:
        return None
    for k, v in fields.items():
        setattr(card, k, v)
    card.updated_at = _utcnow()
    session.commit()
    session.refresh(card)
    return _card_to_dict(card)


def delete_card(session: Session, card_id: int) -> bool:
    card = session.get(Card, card_id)
    if card is None:
        return False
    session.delete(card)
    session.commit()
    return True


def start_timer(session: Session, card_id: int) -> dict | None:
    card = session.get(Card, card_id)
    if card is None:
        return None
    card.timer_running = True
    card.timer_started_at = _utcnow()
    card.updated_at = _utcnow()
    session.commit()
    session.refresh(card)
    return _card_to_dict(card)


def stop_timer(session: Session, card_id: int) -> dict | None:
    card = session.get(Card, card_id)
    if card is None:
        return None
    if card.timer_running and card.timer_started_at:
        started = _ensure_aware(card.timer_started_at)
        elapsed = int((_utcnow() - started).total_seconds())
        card.timer_seconds += elapsed
    card.timer_running = False
    card.timer_started_at = None
    card.updated_at = _utcnow()
    session.commit()
    session.refresh(card)
    return _card_to_dict(card)
