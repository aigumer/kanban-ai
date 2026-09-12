import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app import db as db_module
from app.main import app

# ── Per-test in-memory SQLite (shared across connections via StaticPool) ──────

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(bind=test_engine)


def _override_get_db():
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(autouse=True)
def _setup_db():
    """Create all tables, seed, and drop after each test."""
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    db_module.seed(session)
    session.close()
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def client():
    return TestClient(app, raise_server_exceptions=False)
