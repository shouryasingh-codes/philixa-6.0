from fastapi import APIRouter
from sqlalchemy import text

from app.core.config import get_settings
from app.database.session import SessionLocal
from app.schemas.common import HealthResponse


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    database_status = "ok"
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
    except Exception:
        database_status = "error"
    return HealthResponse(
        status="ok" if database_status == "ok" else "degraded",
        app_version=settings.app_version,
        database=database_status,
    )
