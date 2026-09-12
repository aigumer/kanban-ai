from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class BoardRead(BaseModel):
    id: int
    name: str
    created_at: datetime


class ColumnRead(BaseModel):
    id: int
    board_id: int
    name: str
    position: int


class CardCreate(BaseModel):
    column_id: int
    title: str
    description: str | None = None


class CardUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    position: int | None = None
    column_id: int | None = None


class CardRead(BaseModel):
    id: int
    column_id: int
    title: str
    description: str | None
    position: int
    timer_seconds: int
    timer_running: bool
    timer_started_at: datetime | None
    created_at: datetime
    updated_at: datetime
