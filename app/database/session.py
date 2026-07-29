from __future__ import annotations

from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings
from app.database.base import Base

settings = get_settings()

def _get_async_url(url: str) -> str:
    if url.startswith("sqlite:///"):
        return url.replace("sqlite:///", "sqlite+aiosqlite:///")
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://")
    return url

async_db_url = _get_async_url(settings.database_url)

def _connect_args(database_url: str) -> dict[str, object]:
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}

def _ensure_sqlite_parent(database_url: str) -> None:
    if not database_url.startswith("sqlite"):
        return
    path_value = database_url.split(":///", 1)[-1]
    if path_value.startswith(":memory:"):
        return
    Path(path_value).parent.mkdir(parents=True, exist_ok=True)

_ensure_sqlite_parent(async_db_url)

async_engine = create_async_engine(
    async_db_url,
    connect_args=_connect_args(async_db_url),
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def init_db() -> None:
    from app.models import ai_extraction_log, client, commitment, meeting  # noqa: F401
    
    _ensure_sqlite_parent(async_db_url)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await _apply_sqlite_migrations()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        yield db

async def _apply_sqlite_migrations() -> None:
    if not async_db_url.startswith("sqlite"):
        return
    async with async_engine.begin() as connection:
        client_columns_proxy = await connection.execute(text("PRAGMA table_info(clients)"))
        client_columns = {row[1] for row in client_columns_proxy.fetchall()}
        if "products_owned_json" not in client_columns:
            await connection.execute(
                text("ALTER TABLE clients ADD COLUMN products_owned_json TEXT NOT NULL DEFAULT '[]'")
            )
        commitment_columns_proxy = await connection.execute(text("PRAGMA table_info(commitments)"))
        commitment_columns = {row[1] for row in commitment_columns_proxy.fetchall()}
        if "urgency_level" not in commitment_columns:
            await connection.execute(
                text("ALTER TABLE commitments ADD COLUMN urgency_level VARCHAR(20) NOT NULL DEFAULT 'medium'")
            )
