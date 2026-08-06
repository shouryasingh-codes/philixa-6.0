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
from app.services.live_transcription_service import LiveTranscriptionBuffer

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

    # Step 3: Naya simplified buffer (sirf collect karta hai, infer nahi)
    buffer = LiveTranscriptionBuffer(
        client_names=client_names,
        browser_sample_rate=sample_rate,
    )

    finalized = False  # Day 13: Duplicate stop prevention
    try:
        # Step 4: Browser se audio chunks receive karo — silently collect
        while True:
            message = await websocket.receive()

            if "bytes" in message:
                # Raw PCM audio chunk — buffer mein daalo, kuch aur nahi
                await buffer.add_chunk(message["bytes"])

            elif "text" in message:
                text_data = json.loads(message["text"])

                if text_data.get("action") == "stop" and not finalized:
                    finalized = True  # Day 13: Ek baar se zyada stop nahi chalega
                    logger.info("Stop signal received. Starting full-audio transcription...")

                    # Day 13: Minimum audio duration check (3 seconds)
                    min_duration_seconds = 3.0
                    actual_duration = buffer.total_samples / SAMPLE_RATE
                    if actual_duration < min_duration_seconds:
                        logger.warning(f"Audio too short ({actual_duration:.1f}s) — skipping transcription.")
                        await websocket.send_json({
                            "action": "stopped",
                            "confirmed": "",
                            "is_final": True,
                            "error": f"Recording too short ({actual_duration:.1f}s). Minimum 3 seconds required."
                        })
                        break

                    # UI ko batao ki processing shuru ho gayi
                    await websocket.send_json({"action": "processing"})

                    # Poora audio ek WAV file mein likho
                    wav_path = await buffer.get_full_audio_wav_path()

                    transcript = ""
                    if wav_path:
                        try:
                            from app.services.transcription_service import transcription_service
                            # Exact same call as Audio Upload pipeline — guaranteed accuracy
                            transcript = await asyncio.to_thread(
                                transcription_service.transcribe_audio,
                                wav_path,
                                client_names,
                                diarize,
                            )
                            logger.info(f"Transcription complete: {len(transcript)} chars")
                        except Exception as exc:
                            logger.error(f"Transcription error: {exc}")
                            transcript = ""
                        finally:
                            # Temp WAV file zarur delete karo
                            if os.path.exists(wav_path):
                                os.remove(wav_path)
                                logger.info(f"Temp WAV deleted: {wav_path}")
                    else:
                        logger.warning("No audio collected — empty recording.")

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
        duration = buffer.total_samples / SAMPLE_RATE
        logger.info(f"Live session ended. Total audio collected: {duration:.1f}s")
