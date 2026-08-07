import logging
import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.core.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/voice", tags=["Voice Assistant"])

class SpeakRequest(BaseModel):
    text: str
    model: str = "aura-athena-en" # Default to Athena voice (UK Female)

@router.post("/speak")
async def speak(request: SpeakRequest):
    """
    Text-to-Speech (TTS) endpoint using Deepgram Aura.
    Takes text and returns an audio stream (audio/mpeg) for instant playback.
    """
    settings = get_settings()
    if not settings.deepgram_api_key or settings.transcription_mode != "cloud":
        raise HTTPException(status_code=400, detail="Cloud Voice mode is not enabled or API key missing")
        
    url = f"https://api.deepgram.com/v1/speak?model={request.model}"
    headers = {
        "Authorization": f"Token {settings.deepgram_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": request.text
    }
    
    async def stream_audio():
        async with httpx.AsyncClient() as client:
            try:
                async with client.stream("POST", url, headers=headers, json=payload) as response:
                    if response.status_code != 200:
                        error_text = await response.aread()
                        logger.error(f"Deepgram TTS Error: {response.status_code} - {error_text}")
                        yield b""
                        return
                    
                    async for chunk in response.aiter_bytes():
                        yield chunk
            except Exception as e:
                logger.error(f"Streaming TTS error: {e}")
                yield b""

    return StreamingResponse(stream_audio(), media_type="audio/mpeg")
