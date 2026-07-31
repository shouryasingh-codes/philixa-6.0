import logging
from arq import Retry
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.meeting import Meeting
from app.models.enums import MeetingStatus

logger = logging.getLogger(__name__)

async def process_meeting_transcription(ctx: dict, meeting_id: int, audio_file_path: str) -> bool:
    """
    ARQ Background job to transcribe audio for a meeting.
    This job is meant to run Whisper/WhisperX on the provided audio_file_path.
    """
    logger.info(f"Starting transcription for meeting {meeting_id}, file: {audio_file_path}")
    
    SessionLocal = ctx.get("db_session_factory")
    if not SessionLocal:
        logger.error("db_session_factory not found in context")
        return False
        
    async with SessionLocal() as db:
        # Fetch the meeting
        stmt = select(Meeting).where(Meeting.id == meeting_id)
        result = await db.execute(stmt)
        meeting = result.scalar_one_or_none()
        
        if not meeting:
            logger.error(f"Meeting {meeting_id} not found")
            return False
            
        try:
            # Day 9/10 State Flow: Immediately mark as TRANSCRIBING
            meeting.status = MeetingStatus.TRANSCRIBING.value
            await db.commit()
            
            # Placeholder for actual transcription logic (WhisperX - Day 10)
            # e.g., transcript_text = await asyncio.to_thread(run_whisper, audio_file_path)
            transcript_text = "Simulated transcript for meeting."
            
            # Save transcript to meeting
            meeting.raw_notes = transcript_text
            # Note: Depending on the app's logic, this might also trigger the extraction pipeline here
            
            await db.commit()
            logger.info(f"Successfully transcribed meeting {meeting_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to transcribe meeting {meeting_id}: {str(e)}")
            await db.rollback()
            # Retry if the transcription service fails temporarily
            raise Retry(defer=60)
