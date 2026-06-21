from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.routes_clients import router as clients_router
from app.api.v1.routes_commitments import router as commitments_router
from app.api.v1.routes_health import router as health_router
from app.api.v1.routes_meeting_notes import router as meeting_notes_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.database.session import init_db


settings = get_settings()
configure_logging()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="V1-MVP Commitment and Memory Copilot for Banking Relationship Managers.",
    lifespan=lifespan,
)

WEB_DIR = Path(__file__).resolve().parent / "web"


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


app.include_router(health_router)
app.include_router(meeting_notes_router, prefix="/api/v1")
app.include_router(clients_router, prefix="/api/v1")
app.include_router(commitments_router, prefix="/api/v1")
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")
