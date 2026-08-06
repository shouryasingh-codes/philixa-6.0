import logging
from typing import Any
from datetime import date

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.meeting import Meeting
from app.models.enums import MeetingSourceType, MeetingStatus
from app.services.minio_service import minio_service
from app.core.arq import get_arq_pool

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/audio", tags=["Audio"])

ALLOWED_AUDIO_TYPES = ["audio/mpeg", "audio/mp4", "audio/x-m4a", "audio/wav", "audio/x-wav", "video/mp4"]
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

from app.core.security import get_current_org_id

@router.post("/upload")
async def upload_audio_meeting(
    file: UploadFile = File(...),
    meeting_date: date = Form(...),
    known_client_id: int | None = Form(None),
    db: AsyncSession = Depends(get_db),
    organization_id: str = Depends(get_current_org_id)
) -> Any:
    """
    Upload an audio file (mp3, wav, m4a).
    Validates the file, stores it in MinIO, saves a Meeting record,
    and enqueues an ARQ job for transcription.
    """
    # 1. Validation
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type}. Please upload mp3, m4a, or wav."
        )

    # Calculate file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is too large. Maximum size is 50MB."
        )

    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty."
        )

    # 2. Upload to MinIO (Part 3 integration)
    try:
        object_name = minio_service.upload_audio_file(
            file_data=file.file,
            file_size=file_size,
            content_type=file.content_type,
            original_filename=file.filename
        )
    except Exception as e:
        logger.error(f"MinIO Upload failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to upload audio to storage.")

    # 3. Create Meeting Record in Database (Part 2 integration)
    try:
        new_meeting = Meeting(
            raw_notes="",  # Empty initially, WhisperX will fill this on Day 10
            summary="",
            meeting_date=meeting_date,
            source_type=MeetingSourceType.AUDIO_UPLOAD.value,
            status=MeetingStatus.QUEUED.value,
            audio_path=object_name,
            # Note: client identification might be required later, but for now we proceed with standard flow
            client_identification_status="identified", 
            client_identification_confidence=1.0
        )
        
        db.add(new_meeting)
        await db.commit()
        await db.refresh(new_meeting)
    except Exception as e:
        logger.error(f"Database insertion failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save meeting record.")

    # 4. Enqueue ARQ Background Job (Day 8 integration)
    try:
        redis_pool = get_arq_pool()
        if not redis_pool:
            logger.warning("Redis pool not found. Job was not enqueued.")
            raise Exception("Redis pool is not initialized.")
            
        # Enqueue the job matching Day 8's function name: process_meeting_transcription
        await redis_pool.enqueue_job(
            "process_meeting_transcription", 
            meeting_id=new_meeting.id,
            audio_file_path=object_name,
            known_client_id=known_client_id,
            organization_id=organization_id
        )
        logger.info(f"Enqueued process_meeting_transcription job for meeting {new_meeting.id}")
    except Exception as e:
        logger.error(f"ARQ Enqueue failed: {e}")
        # Note: In production we might want to clean up the DB record and MinIO object if this fails,
        # but for V1 MVP we log the error and return a 500.
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to enqueue background processing.")

    return {
        "message": "Audio uploaded successfully. Transcription queued.",
        "meeting_id": new_meeting.id,
        "status": new_meeting.status
    }
