from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import db
from app.database import get_db
from app.schemas import BoardRead, CardCreate, CardRead, CardUpdate, ColumnRead

router = APIRouter(prefix="/api")


# --- Board -------------------------------------------------------------------

@router.get("/board", response_model=BoardRead)
def get_board(session: Session = Depends(get_db)):
    board = db.get_board(session)
    if board is None:
        raise HTTPException(404, "No board found")
    return board


# --- Columns -----------------------------------------------------------------

@router.get("/columns", response_model=list[ColumnRead])
def list_columns(session: Session = Depends(get_db)):
    return db.get_columns(session)


# --- Cards -------------------------------------------------------------------

@router.get("/cards", response_model=list[CardRead])
def list_cards(
    column_id: int | None = Query(None),
    session: Session = Depends(get_db),
):
    return db.get_cards(session, column_id)


@router.post("/cards", response_model=CardRead, status_code=201)
def create_card(body: CardCreate, session: Session = Depends(get_db)):
    return db.create_card(session, body.column_id, body.title, body.description)


@router.patch("/cards/{card_id}", response_model=CardRead)
def update_card(card_id: int, body: CardUpdate, session: Session = Depends(get_db)):
    fields = {k: v for k, v in body.model_dump().items() if k in body.model_fields_set}
    card = db.update_card(session, card_id, **fields)
    if card is None:
        raise HTTPException(404, f"Card {card_id} not found")
    return card


@router.delete("/cards/{card_id}", status_code=204)
def delete_card(card_id: int, session: Session = Depends(get_db)):
    if not db.delete_card(session, card_id):
        raise HTTPException(404, f"Card {card_id} not found")


# --- Timer -------------------------------------------------------------------

@router.post("/cards/{card_id}/timer/start", response_model=CardRead)
def start_timer(card_id: int, session: Session = Depends(get_db)):
    card = db.start_timer(session, card_id)
    if card is None:
        raise HTTPException(404, f"Card {card_id} not found")
    return card


@router.post("/cards/{card_id}/timer/stop", response_model=CardRead)
def stop_timer(card_id: int, session: Session = Depends(get_db)):
    card = db.stop_timer(session, card_id)
    if card is None:
        raise HTTPException(404, f"Card {card_id} not found")
    return card
