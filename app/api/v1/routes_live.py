"""
Day 12 (Accuracy Fix) + Day 13 (Robustness): Live Audio Collection WebSocket Route
Simplified: No chunk inference loop, no watchdog.
Browser audio is silently collected in buffer.
On stop: full audio → WAV → transcription_service (same as Audio Upload) → result.
Day 13 additions: Duplicate stop prevention, minimum audio duration check.
"""

import asyncio
import json
import logging
import os

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from sqlalchemy import select

from app.database.session import AsyncSessionLocal
from app.models.client import Client


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/live", tags=["Live Transcription"])

SAMPLE_RATE = 16000


@router.websocket("/transcribe")
async def live_transcribe(
    websocket: WebSocket,
    api_key: str = Query(...),
    sample_rate: int = Query(default=16000),
    diarize: bool = Query(default=False),  # False=Solo (fast), True=Meeting (with speaker labels)
) -> None:
    """
    Live audio collection WebSocket endpoint.
    Browser AudioWorklet se raw Int16 PCM bytes receive karta hai.
    Audio silently buffer mein collect hota hai (no live inference).
    Stop signal par: full audio → WAV → Whisper (one-shot) → transcript.
    """
    # Step 1: API key validate karo
    from app.core.config import get_settings
    settings = get_settings()
    if api_key not in [settings.api_key, settings.demo_api_key]:
        await websocket.close(code=1008, reason="Invalid API key")
        return

    await websocket.accept()
    logger.info(f"Live WebSocket connected. Browser sample rate: {sample_rate}Hz")

    # Step 2: DB se client names fetch karo (Whisper prompt injection ke liye)
    client_names: list[str] = []
    async with AsyncSessionLocal() as db:
        result = await db.scalars(select(Client.name))
        client_names = [n for n in result.all() if n]
    logger.info(f"Loaded {len(client_names)} client names for prompt injection.")

    # Step 3: Initialize Strategy based on configuration
    from app.services.live_strategies import LocalTranscriptionSession, DeepgramTranscriptionSession
    
    if settings.transcription_mode == "cloud" and settings.deepgram_api_key:
        logger.info("Using Deepgram Cloud Transcription Strategy")
        session = DeepgramTranscriptionSession(
            api_key=settings.deepgram_api_key,
            sample_rate=sample_rate,
            diarize=diarize
        )
        await session.initialize()
    else:
        logger.info("Using Local Whisper Transcription Strategy")
        session = LocalTranscriptionSession(
            client_names=client_names,
            sample_rate=sample_rate,
            diarize=diarize
        )
        await session.initialize()
        
    total_bytes_received = 0

    finalized = False  # Day 13: Duplicate stop prevention
    try:
        # Step 4: Browser se audio chunks receive karo — silently collect
        while True:
            message = await websocket.receive()

            if "bytes" in message:
                # Raw PCM audio chunk — pass to strategy
                chunk = message["bytes"]
                total_bytes_received += len(chunk)
                await session.add_chunk(chunk)

            elif "text" in message:
                text_data = json.loads(message["text"])

                if text_data.get("action") == "stop" and not finalized:
                    finalized = True  # Day 13: Ek baar se zyada stop nahi chalega
                    logger.info("Stop signal received. Starting full-audio transcription...")

                    # Day 13: Minimum audio duration check (1.0 seconds for short voice queries)
                    min_duration_seconds = 1.0
                    actual_duration = (total_bytes_received / 2) / sample_rate # 16-bit PCM
                    if actual_duration < min_duration_seconds:
                        logger.warning(f"Audio too short ({actual_duration:.1f}s) — skipping transcription.")
                        await websocket.send_json({
                            "action": "stopped",
                            "confirmed": "",
                            "is_final": True,
                            "error": f"Recording too short ({actual_duration:.1f}s). Minimum 1 second required."
                        })
                        break

                    # UI ko batao ki processing shuru ho gayi
                    await websocket.send_json({"action": "processing"})

                    # Finish the session and get the transcript
                    try:
                        transcript = await session.finish()
                        logger.info(f"Transcription complete: {len(transcript)} chars")
                    except Exception as exc:
                        logger.error(f"Transcription error: {exc}")
                        transcript = ""

                    # Final result browser ko bhejo
                    await websocket.send_json({
                        "action": "stopped",
                        "confirmed": transcript.strip(),
                        "is_final": True,
                    })
                    break

    except WebSocketDisconnect:
        logger.info("Live WebSocket disconnected cleanly.")
    except Exception as exc:
        logger.error(f"WebSocket unexpected error: {exc}")
    finally:
        duration = (total_bytes_received / 2) / sample_rate if 'total_bytes_received' in locals() else 0
        logger.info(f"Live session ended. Total audio collected: {duration:.1f}s")
