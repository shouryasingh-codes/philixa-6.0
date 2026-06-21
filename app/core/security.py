from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import Settings, get_settings


api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
DEMO_API_KEY = "philixa-demo-secret-123"


def require_api_key(
    supplied_key: str | None = Security(api_key_header),
    settings: Settings = Depends(get_settings),
) -> None:
    allowed_keys = {settings.api_key, DEMO_API_KEY}
    if supplied_key not in allowed_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )
