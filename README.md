# Kanban Board

A lightweight kanban board with drag-and-drop cards, CRUD, and a per-task work timer.

## Tech Stack

- **Backend:** Python 3.11+, FastAPI, SQLAlchemy, uv (package manager)
- **Frontend:** Vue 3, Vite, TypeScript, vuedraggable
- **Database:** SQLite (default), PostgreSQL supported via `DATABASE_URL` env var

## Quick Start

```bash
make dev
```

Frontend: `http://localhost:5173` | Backend: `http://localhost:8000`

## Manual Setup

```bash
# Install dependencies
cd backend && uv sync
cd ../frontend && npm install

# Run backend (terminal 1)
cd backend
uv run uvicorn app.main:app --reload

# Run frontend (terminal 2)
cd frontend
npm run dev
```

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/board` | Get board info |
| GET | `/api/columns` | List columns |
| GET | `/api/cards?column_id=` | List cards |
| POST | `/api/cards` | Create card |
| PATCH | `/api/cards/{id}` | Update card |
| DELETE | `/api/cards/{id}` | Delete card |
| POST | `/api/cards/{id}/timer/start` | Start timer |
| POST | `/api/cards/{id}/timer/stop` | Stop timer |

## Tests

```bash
cd backend
uv run pytest -v
```

## Database

Set `DATABASE_URL` to switch from SQLite to PostgreSQL:

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/kanban"
```
