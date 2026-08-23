from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.routes_audio import router as audio_router
from app.api.v1.routes_auth import router as auth_router, ws_ticket_router
from app.api.v1.routes_clients import router as clients_router
from app.api.v1.routes_commitments import router as commitments_router
from app.api.v1.routes_dashboard import router as dashboard_router
from app.api.v1.routes_health import router as health_router
from app.api.v1.routes_jobs import router as jobs_router
from app.api.v1.routes_live import router as live_router
from app.api.v1.routes_meeting_notes import router as meeting_notes_router
from app.api.v1.routes_preferences import router as preferences_router
from app.api.v1.routes_voice import router as voice_router
from app.api.v1.routes_webhooks import router as webhooks_router
from app.api.v1.routes_workspace import router as workspace_router
from app.core.config import get_settings
from app.core.csrf import CSRFProtectionMiddleware
from app.core.lifespan import lifespan as core_lifespan
from app.core.logging import configure_logging
from app.database.session import init_db

settings = get_settings()
configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    if not settings.skip_startup_checks:
        await init_db()
    async with core_lifespan(app):
        yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="PHILIXA 6.0 Multi-Tenant SaaS Authentication & Copilot System.",
    lifespan=lifespan,
)

# 1. CORS Middleware
if settings.allowed_origins:
    origins = (
        settings.allowed_origins
        if isinstance(settings.allowed_origins, list)
        else [o.strip() for o in settings.allowed_origins.split(",") if o.strip()]
    )
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

# 2. CSRF Protection Middleware
app.add_middleware(CSRFProtectionMiddleware)

WEB_DIR = Path(__file__).resolve().parent / "web"


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


# 3. Public Health Router
app.include_router(health_router)

# 4. Auth & Workspace Routers (Dual-mounted at root and /api/v1 for test & API compatibility)
app.include_router(auth_router)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(workspace_router)
app.include_router(workspace_router, prefix="/api/v1")

# 5. Core API Routers (/api/v1)
app.include_router(meeting_notes_router, prefix="/api/v1")
app.include_router(clients_router, prefix="/api/v1")
app.include_router(commitments_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(preferences_router, prefix="/api/v1")
app.include_router(webhooks_router, prefix="/api/v1")
app.include_router(jobs_router, prefix="/api/v1")
app.include_router(audio_router)
app.include_router(audio_router, prefix="/api/v1")
app.include_router(live_router)
app.include_router(live_router, prefix="/api/v1")
app.include_router(voice_router, prefix="/api/v1")
app.include_router(ws_ticket_router)
app.include_router(ws_ticket_router, prefix="/api/v1")

# 6. Static Files
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")
