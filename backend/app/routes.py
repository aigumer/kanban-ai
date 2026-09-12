from fastapi import APIRouter, HTTPException, Query

from app import db
from app.schemas import BoardRead, CardCreate, CardRead, CardUpdate, ColumnRead

router = APIRouter(prefix="/api")


# --- Board -------------------------------------------------------------------

@router.get("/board", response_model=BoardRead)
def get_board():
    board = db.get_board()
    if board is None:
        raise HTTPException(404, "No board found")
    return board


# --- Columns -----------------------------------------------------------------

@router.get("/columns", response_model=list[ColumnRead])
def list_columns():
    return db.get_columns()


# --- Cards -------------------------------------------------------------------

@router.get("/cards", response_model=list[CardRead])
def list_cards(column_id: int | None = Query(None)):
    return db.get_cards(column_id)


@router.post("/cards", response_model=CardRead, status_code=201)
def create_card(body: CardCreate):
    return db.create_card(body.column_id, body.title, body.description)


@router.patch("/cards/{card_id}", response_model=CardRead)
def update_card(card_id: int, body: CardUpdate):
    card = db.update_card(
        card_id,
        title=body.title,
        description=body.description,
        position=body.position,
        column_id=body.column_id,
    )
    if card is None:
        raise HTTPException(404, f"Card {card_id} not found")
    return card


@router.delete("/cards/{card_id}", status_code=204)
def delete_card(card_id: int):
    if not db.delete_card(card_id):
        raise HTTPException(404, f"Card {card_id} not found")


# --- Timer -------------------------------------------------------------------

@router.post("/cards/{card_id}/timer/start", response_model=CardRead)
def start_timer(card_id: int):
    card = db.start_timer(card_id)
    if card is None:
        raise HTTPException(404, f"Card {card_id} not found")
    return card


@router.post("/cards/{card_id}/timer/stop", response_model=CardRead)
def stop_timer(card_id: int):
    card = db.stop_timer(card_id)
    if card is None:
        raise HTTPException(404, f"Card {card_id} not found")
    return card
