import asyncio

from arq import create_pool
from arq.connections import RedisSettings

from app.core.config import get_settings


async def main() -> None:
    pool = await create_pool(RedisSettings.from_dsn(get_settings().redis_url))
    try:
        await pool.enqueue_job(
            "process_meeting_transcription",
            meeting_id=152,
            audio_file_path="meetings/38cec6ab-7e74-47d6-ab22-b2bc550c0304.m4a",
            known_client_id=76,
            _job_id="retry_audio_meeting_152_hindi_transcription",
        )
    finally:
        await pool.aclose()


asyncio.run(main())
