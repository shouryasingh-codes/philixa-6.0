import abc
import asyncio
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

class LiveTranscriptionSession(abc.ABC):
    """Unified interface for real-time and local audio processing."""
    
    @abc.abstractmethod
    async def add_chunk(self, pcm_bytes: bytes) -> None:
        pass

    @abc.abstractmethod
    async def finish(self) -> str:
        pass


class LocalTranscriptionSession(LiveTranscriptionSession):
    def __init__(self, client_names: list[str], sample_rate: int, diarize: bool):
        from app.services.live_transcription_service import LiveTranscriptionBuffer
        self.buffer = LiveTranscriptionBuffer(client_names=client_names, browser_sample_rate=sample_rate)
        self.client_names = client_names
        self.diarize = diarize

    async def initialize(self) -> None:
        # Local buffer doesn't need async startup
        pass

    async def add_chunk(self, pcm_bytes: bytes) -> None:
        await self.buffer.add_chunk(pcm_bytes)

    async def finish(self) -> str:
        wav_path = await self.buffer.get_full_audio_wav_path()
        transcript = ""
        if wav_path:
            try:
                from app.services.transcription_service import transcription_service
                transcript = await asyncio.to_thread(
                    transcription_service.transcribe_audio,
                    wav_path,
                    self.client_names,
                    self.diarize,
                )
                logger.info(f"Local Transcription complete: {len(transcript)} chars")
            except Exception as exc:
                logger.error(f"Local Transcription error: {exc}")
            finally:
                if os.path.exists(wav_path):
                    os.remove(wav_path)
                    logger.info(f"Temp WAV deleted: {wav_path}")
        return transcript.strip()


class DeepgramTranscriptionSession(LiveTranscriptionSession):
    def __init__(self, api_key: str, sample_rate: int, diarize: bool):
        from deepgram import DeepgramClient
        self.deepgram = DeepgramClient(api_key=api_key)
        self.dg_connection = self.deepgram.listen.asynclive.v("1")
        self.sample_rate = sample_rate
        self.diarize = diarize
        self.transcript_buffer = []
        self.is_finished = False

    async def initialize(self) -> None:
        from deepgram import LiveTranscriptionEvents, LiveOptions
        
        async def on_message(self_conn, result, **kwargs):
            try:
                if result.channel and result.channel.alternatives:
                    sentence = result.channel.alternatives[0].transcript
                    if sentence:
                        self.transcript_buffer.append(sentence)
                        logger.info(f"Deepgram live transcript: {sentence}")
            except Exception as e:
                logger.error(f"Deepgram message parsing error: {e}")

        async def on_error(self_conn, error, **kwargs):
            logger.error(f"Deepgram Error: {error}")

        async def on_close(self_conn, close, **kwargs):
            logger.info("Deepgram Connection Closed")

        self.dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        self.dg_connection.on(LiveTranscriptionEvents.Error, on_error)
        self.dg_connection.on(LiveTranscriptionEvents.Close, on_close)

        options = LiveOptions(
            model="nova-2",
            language="hi", # Use Hindi model for perfect Hinglish transcription
            smart_format=True,
            encoding="linear16",
            channels=1,
            sample_rate=self.sample_rate,
            diarize=self.diarize,
            interim_results=False # We only need finalized sentences for the buffer
        )
        
        success = await self.dg_connection.start(options)
        if not success:
            logger.error("Failed to connect to Deepgram")
            raise RuntimeError("Deepgram connection failed")

    async def add_chunk(self, pcm_bytes: bytes) -> None:
        if not hasattr(self, 'raw_audio_buffer'):
            self.raw_audio_buffer = bytearray()
        self.raw_audio_buffer.extend(pcm_bytes)
        
        if not self.is_finished:
            try:
                await self.dg_connection.send(pcm_bytes)
            except Exception as e:
                logger.error(f"Error sending bytes to Deepgram: {e}")

    async def finish(self) -> str:
        self.is_finished = True
        try:
            await self.dg_connection.finish()
        except Exception as e:
            logger.error(f"Error closing Deepgram connection: {e}")
        
        # Small delay to ensure all pending transcripts from the websocket are parsed
        await asyncio.sleep(0.5)
        return " ".join(self.transcript_buffer).strip()
