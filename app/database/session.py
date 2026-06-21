from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings
from app.database.base import Base


settings = get_settings()


def _connect_args(database_url: str) -> dict[str, object]:
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


def _ensure_sqlite_parent(database_url: str) -> None:
    if not database_url.startswith("sqlite:///"):
        return
    path_value = database_url.replace("sqlite:///", "", 1)
    if path_value.startswith(":memory:"):
        return
    Path(path_value).parent.mkdir(parents=True, exist_ok=True)


_ensure_sqlite_parent(settings.database_url)
engine = create_engine(
    settings.database_url,
    connect_args=_connect_args(settings.database_url),
    future=True,
)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True,
)


def init_db() -> None:
    from app.models import ai_extraction_log, client, commitment, meeting  # noqa: F401

    _ensure_sqlite_parent(settings.database_url)
    Base.metadata.create_all(bind=engine)
    _apply_sqlite_migrations()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _apply_sqlite_migrations() -> None:
    if not settings.database_url.startswith("sqlite"):
        return
    with engine.begin() as connection:
        client_columns = {
            row[1] for row in connection.execute(text("PRAGMA table_info(clients)")).fetchall()
        }
        if "products_owned_json" not in client_columns:
            connection.execute(
                text(
                    "ALTER TABLE clients ADD COLUMN products_owned_json TEXT NOT NULL DEFAULT '[]'"
                )
            )
        commitment_columns = {
            row[1]
            for row in connection.execute(text("PRAGMA table_info(commitments)")).fetchall()
        }
        if "urgency_level" not in commitment_columns:
            connection.execute(
                text(
                    "ALTER TABLE commitments ADD COLUMN urgency_level VARCHAR(20) NOT NULL DEFAULT 'medium'"
                )
            )
