import logging
import httpx
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Optional
from app.core.config import get_settings
from app.database.session import get_db
from app.services.voice_assistant import VoiceAssistantService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/voice", tags=["Voice Assistant"])

class SpeakRequest(BaseModel):
    text: str
    model: str = "aura-asteria-en" # Default to Asteria voice (US Female) - slightly more neutral

class ChatRequest(BaseModel):
    text: str
    conversation_history: Optional[List[Dict[str, str]]] = None

@router.post("/speak")
async def speak(request: SpeakRequest):
    """
    Text-to-Speech (TTS) endpoint using Deepgram Aura.
    Takes text and returns an audio stream (audio/mpeg) for instant playback.
    """
    settings = get_settings()
    if not settings.deepgram_api_key or settings.transcription_mode != "cloud":
        raise HTTPException(status_code=400, detail="Cloud Voice mode is not enabled or API key missing")
        
    if settings.sarvam_api_key:
        import base64
        import json
        
        # Override model to Sarvam's bulbul:v3
        url = "https://api.sarvam.ai/text-to-speech"
        headers = {
            "api-subscription-key": settings.sarvam_api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": [request.text],
            "target_language_code": "hi-IN",
            "speaker": "shreya",
            "pitch": 0,
            "pace": 1.15,
            "loudness": 1.5,
            "speech_sample_rate": 8000,
            "enable_preprocessing": True,
            "model": "bulbul:v1"
        }
        
        # Note: The search results mentioned bulbul:v3 structure, but the actual bulbul:v1 TTS API for Sarvam is structured slightly differently. Let's use the standard bulbul:v3 structure provided in the research.
        payload = {
            "text": request.text,
            "language_code": "hi-IN",
            "speaker": "shreya",
            "model": "bulbul:v3"
        }
        
        async def stream_sarvam_audio():
            async with httpx.AsyncClient(timeout=30.0) as client:
                try:
                    response = await client.post(url, headers=headers, json=payload)
                    if response.status_code != 200:
                        logger.error(f"Sarvam TTS Error: {response.status_code} - {response.text}")
                        yield b""
                        return
                    
                    data = response.json()
                    if "audios" in data and len(data["audios"]) > 0:
                        # Sarvam returns base64 string
                        audio_base64 = data["audios"][0]
                        audio_bytes = base64.b64decode(audio_base64)
                        yield audio_bytes
                    else:
                        logger.error("No audio returned from Sarvam API")
                        yield b""
                except Exception as e:
                    logger.error(f"Sarvam TTS exception: {e}")
                    yield b""
                    
        return StreamingResponse(stream_sarvam_audio(), media_type="audio/wav")

    # Fallback: Deepgram Aura
    url = f"https://api.deepgram.com/v1/speak?model={request.model}"
    headers = {
        "Authorization": f"Token {settings.deepgram_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": request.text
    }
    
    async def stream_audio():
        async with httpx.AsyncClient(timeout=30.0) as client:
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

@router.post("/chat")
async def chat_with_assistant(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Takes user's transcribed voice text, processes it through the VoiceAssistant LLM,
    and returns a conversational text response.
    """
    settings = get_settings()
    assistant = VoiceAssistantService(db, settings)
    
    response_text = await assistant.chat(request.text, request.conversation_history)
    return {"response": response_text}
