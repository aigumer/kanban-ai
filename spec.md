# Mini Kanban Board — Specification

## Overview

A lightweight kanban board with drag-and-drop cards, basic CRUD, and a per-task work timer.

## Tech Stack

- **Backend:** Python (uv) — REST API (FastAPI)
- **Frontend:** Vue 3 + Vite + TypeScript
- **Database:** SQLite (default) with option for PostgreSQL

## Columns (fixed)

1. To Do
2. In Progress
3. Done

## Data Model

### Board
- `id` (int, PK)
- `name` (string)
- `created_at` (datetime)

### Column
- `id` (int, PK)
- `board_id` (int, FK → Board)
- `name` (string)
- `position` (int)

### Card
- `id` (int, PK)
- `column_id` (int, FK → Column)
- `title` (string)
- `description` (text, nullable)
- `position` (int)
- `timer_seconds` (int, default 0) — accumulated work time
- `timer_running` (bool, default false)
- `timer_started_at` (datetime, nullable)
- `created_at` (datetime)
- `updated_at` (datetime)

## API Endpoints (REST)

### Cards
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cards?column_id=` | List cards in a column |
| POST | `/api/cards` | Create a card |
| PATCH | `/api/cards/{id}` | Update card (title, description, position, column) |
| DELETE | `/api/cards/{id}` | Delete a card |
| POST | `/api/cards/{id}/timer/start` | Start work timer |
| POST | `/api/cards/{id}/timer/stop` | Stop work timer, accumulate time |

### Columns
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/columns` | List all columns |

### Board
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/board` | Get board info (auto-create default on first call) |

## Frontend Pages

- `/` — Single board view with 3 columns
- Cards rendered in columns, draggable between them

## Features

1. **Drag & Drop** — Move cards between To Do / In Progress / Done (vue-draggable)
2. **CRUD** — Create, edit (inline or modal), delete cards
3. **Work Timer** — Per-card start/stop button; displays elapsed time (HH:MM:SS); persists on backend
4. **Responsive** — Works on desktop; basic mobile support

## Seed Data

On first launch, create:
- Board: "My Board"
- Columns: To Do, In Progress, Done
- No sample cards

## Running

```bash
# Backend
cd backend
uv sync
uv run uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

Frontend proxies `/api` → `http://localhost:8000`.
