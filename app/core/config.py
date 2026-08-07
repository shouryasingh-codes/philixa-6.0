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
    redis_url: str
    api_key: str
    demo_api_key: str
    # Primary provider (legacy / single-provider path)
    ai_provider: str
    ai_model: str
    ai_api_key: str
    ai_base_url: str
    ai_timeout_seconds: int

    # Dual-provider fallback system
    ai_economy_provider: str
    ai_economy_model: str
    ai_review_provider: str
    ai_review_model: str
    # Per-provider API keys
    groq_api_key: str
    gemini_api_key: str
    # Notifications
    notification_mode: str
    smtp_hostname: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    smtp_use_tls: bool
    smtp_from_address: str
    # WhatsApp Cloud API
    whatsapp_phone_number_id: str
    whatsapp_business_account_id: str
    whatsapp_access_token: str
    whatsapp_verify_token: str
    # Misc
    prompt_version: str
    raw_notes_max_chars: int
    client_name_max_chars: int
    commitment_description_max_chars: int
    client_auto_match_threshold: float
    client_auto_create_threshold: float
    due_date_threshold: float
    skip_startup_checks: bool
    embedding_model: str
    # MinIO Audio Storage (Day 9 & Day 10 Prep)
    minio_url: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket_name: str
    retain_audio_files: bool
    
    # HuggingFace
    hf_token: str
    
    # Voice AI Architecture
    transcription_mode: str = "local"
    deepgram_api_key: str = ""

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
        database_url=os.getenv("PHILIXA_DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/philixa"),
        redis_url=os.getenv("PHILIXA_REDIS_URL", "redis://localhost:6379/0"),
        api_key=os.getenv("PHILIXA_API_KEY", "dev-api-key"),
        demo_api_key=os.getenv("PHILIXA_DEMO_API_KEY", ""),
        # Primary provider
        ai_provider=os.getenv("PHILIXA_AI_PROVIDER", "groq").lower().strip(),
        ai_model=os.getenv("PHILIXA_AI_MODEL", "llama-3.3-70b-versatile").strip(),
        ai_api_key=os.getenv("PHILIXA_AI_API_KEY", "").strip(),
        ai_base_url=os.getenv("PHILIXA_AI_BASE_URL", "").strip(),
        ai_timeout_seconds=_env_int("PHILIXA_AI_TIMEOUT_SECONDS", 20),
        # Dual-provider fallback
        ai_economy_provider=os.getenv("PHILIXA_AI_ECONOMY_PROVIDER", "groq").lower().strip(),
        ai_economy_model=os.getenv("PHILIXA_AI_ECONOMY_MODEL", "llama-3.3-70b-versatile").strip(),
        ai_review_provider=os.getenv("PHILIXA_AI_REVIEW_PROVIDER", "gemini").lower().strip(),
        ai_review_model=os.getenv("PHILIXA_AI_REVIEW_MODEL", "gemini-2.5-flash").strip(),
        # Per-provider keys
        groq_api_key=os.getenv("PHILIXA_GROQ_API_KEY", "").strip(),
        gemini_api_key=os.getenv("PHILIXA_GEMINI_API_KEY", "").strip(),
        # Notifications
        notification_mode=os.getenv("PHILIXA_NOTIFICATION_MODE", "whatsapp").lower().strip(),
        smtp_hostname=os.getenv("PHILIXA_SMTP_HOSTNAME", "smtp.gmail.com").strip(),
        smtp_port=_env_int("PHILIXA_SMTP_PORT", 587),
        smtp_username=os.getenv("PHILIXA_SMTP_USERNAME", "").strip(),
        smtp_password=os.getenv("PHILIXA_SMTP_PASSWORD", "").strip(),
        smtp_use_tls=os.getenv("PHILIXA_SMTP_USE_TLS", "1") == "1",
        smtp_from_address=os.getenv("PHILIXA_SMTP_FROM_ADDRESS", "no-reply@philixa.com").strip(),
        # WhatsApp Cloud API
        whatsapp_phone_number_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID", "").strip(),
        whatsapp_business_account_id=os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID", "").strip(),
        whatsapp_access_token=os.getenv("WHATSAPP_ACCESS_TOKEN", "").strip(),
        whatsapp_verify_token=os.getenv("WHATSAPP_VERIFY_TOKEN", "").strip(),
        # Misc
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
        skip_startup_checks=os.getenv("PHILIXA_SKIP_STARTUP_CHECKS", "0") == "1",
        embedding_model=os.getenv("PHILIXA_EMBEDDING_MODEL", "intfloat/multilingual-e5-small").strip(),
        # MinIO Audio Storage
        minio_url=os.getenv("PHILIXA_MINIO_URL", "localhost:9000").strip(),
        minio_access_key=os.getenv("PHILIXA_MINIO_ACCESS_KEY", "philixa_minio").strip(),
        minio_secret_key=os.getenv("PHILIXA_MINIO_SECRET_KEY", "philixa_secret").strip(),
        minio_bucket_name=os.getenv("PHILIXA_MINIO_BUCKET_NAME", "philixa-audio").strip(),
        retain_audio_files=os.getenv("PHILIXA_RETAIN_AUDIO", "0") == "1",
        # HuggingFace Token
        hf_token=os.getenv("PHILIXA_HF_TOKEN", "").strip(),
        # Voice AI Architecture
        transcription_mode=os.getenv("PHILIXA_TRANSCRIPTION_MODE", "local").strip(),
        deepgram_api_key=os.getenv("PHILIXA_DEEPGRAM_API_KEY", "").strip(),
    )
