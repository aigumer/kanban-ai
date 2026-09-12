.PHONY: dev install install-backend install-frontend

dev: install
	@cd backend && uv run uvicorn app.main:app --reload &
	@cd frontend && npm run dev

install: install-backend install-frontend

install-backend:
	cd backend && uv sync

install-frontend:
	cd frontend && npm install
