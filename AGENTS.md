## Project

Kanban board with drag-and-drop, CRUD, and per-card work timer.

## Structure

```
├── backend/          FastAPI + SQLAlchemy (Python, uv)
│   ├── app/
│   │   ├── main.py       App entrypoint
│   │   ├── routes.py     API endpoints
│   │   ├── models.py     SQLAlchemy ORM models
│   │   ├── schemas.py    Pydantic request/response schemas
│   │   ├── database.py   Engine/session setup
│   │   └── db.py         Database operations
│   └── tests/
│       ├── conftest.py   Test DB setup (in-memory SQLite)
│       └── test_api.py   Endpoint tests
├── frontend/         Vue 3 + Vite + TypeScript
│   └── src/
│       ├── api/          Backend API client
│       ├── components/   Vue components (Board, Column, Card, Modal)
│       └── types.ts      Shared TypeScript interfaces
├── _docs/spec.md     Original specification
└── Makefile
```

## Commands

- `make dev` — run both backend + frontend
- `uv run pytest -v` — run backend tests (from `backend/`)

## Conventions

- Backend: snake_case, Pydantic for validation, SQLAlchemy ORM
- Frontend: TypeScript, Composition API (`<script setup>`)
- API calls centralized in `frontend/src/api/index.ts`
- Database ops centralized in `backend/app/db.py`
- Tests use per-test in-memory SQLite with `StaticPool`
