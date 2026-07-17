from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_version: str
    database_url: str
    api_key: str
    ai_provider: str
    ai_model: str
    ai_api_key: str
    ai_base_url: str
    ai_timeout_seconds: int
    prompt_version: str
    raw_notes_max_chars: int
    client_name_max_chars: int
    commitment_description_max_chars: int
    client_auto_match_threshold: float
    client_auto_create_threshold: float
    due_date_threshold: float


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return int(value)


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return float(value)


@lru_cache
def get_settings() -> Settings:
    load_dotenv()
    return Settings(
        app_name=os.getenv("PHILIXA_APP_NAME", "PHILIXA 6.0 V1-MVP"),
        app_version=os.getenv("PHILIXA_APP_VERSION", "1.0.0"),
        database_url=os.getenv("PHILIXA_DATABASE_URL", "sqlite:///./data/philixa.db"),
        api_key=os.getenv("PHILIXA_API_KEY", "dev-api-key"),
        ai_provider=os.getenv("PHILIXA_AI_PROVIDER", "local").lower().strip(),
        ai_model=os.getenv("PHILIXA_AI_MODEL", "local-heuristic-v1").strip(),
        ai_api_key=os.getenv("PHILIXA_AI_API_KEY", "").strip(),
        ai_base_url=os.getenv("PHILIXA_AI_BASE_URL", "").strip(),
        ai_timeout_seconds=_env_int("PHILIXA_AI_TIMEOUT_SECONDS", 20),
        prompt_version=os.getenv("PHILIXA_PROMPT_VERSION", "v1-mvp-2026-06-19"),
        raw_notes_max_chars=_env_int("PHILIXA_RAW_NOTES_MAX_CHARS", 10000),
        client_name_max_chars=_env_int("PHILIXA_CLIENT_NAME_MAX_CHARS", 120),
        commitment_description_max_chars=_env_int(
            "PHILIXA_COMMITMENT_DESCRIPTION_MAX_CHARS", 500
        ),
        client_auto_match_threshold=_env_float(
            "PHILIXA_CLIENT_AUTO_MATCH_THRESHOLD", 0.85
        ),
        client_auto_create_threshold=_env_float(
            "PHILIXA_CLIENT_AUTO_CREATE_THRESHOLD", 0.80
        ),
        due_date_threshold=_env_float("PHILIXA_DUE_DATE_THRESHOLD", 0.75),
    )
