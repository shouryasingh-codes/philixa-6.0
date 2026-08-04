from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.provider import AIExtractionError
from app.core.security import require_api_key
from app.database.session import get_db
from app.schemas.meeting_note import (
    ClientConfirmationRequest,
    ClientConfirmationResponse,
    MeetingNoteProcessRequest,
    MeetingNoteProcessResponse,
)
from app.services.meeting_processing_service import MeetingProcessingService
from pydantic import BaseModel, Field
from app.models.enums import MeetingStatus
from app.core.arq import get_arq_pool


class TranscriptUpdate(BaseModel):
    raw_notes: str = Field(..., description="The corrected meeting transcript")

router = APIRouter(
    prefix="/meeting-notes",
    tags=["meeting notes"],
    dependencies=[Depends(require_api_key)],
)


@router.post("/process", response_model=MeetingNoteProcessResponse)
async def process_meeting_note(
    request: Annotated[
        MeetingNoteProcessRequest,
        Body(
            openapi_examples={
                "clear_client": {
                    "summary": "Clear client with due dates",
                    "value": {
                        "raw_notes": "Met Rajesh Sharma today. Interested in business loan. Concerned about processing time. Promised documents by Friday. Asked for approval status update in 3 days.",
                        "meeting_date": "2026-06-19",
                    },
                },
                "ambiguous_client": {
                    "summary": "Ambiguous client requiring confirmation",
                    "value": {
                        "raw_notes": "Customer interested in home loan. Wants callback Friday.",
                        "meeting_date": "2026-06-19",
                    },
                },
            }
        ),
    ],
    db: AsyncSession = Depends(get_db),
) -> dict:
    try:
        return await MeetingProcessingService().process_notes(db, request)
    except AIExtractionError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc


@router.post("/{meeting_id}/confirm-client", response_model=ClientConfirmationResponse)
async def confirm_client(
    meeting_id: int,
    request: Annotated[
        ClientConfirmationRequest,
        Body(
            openapi_examples={
                "select_existing_client": {
                    "summary": "Attach to an existing client",
                    "value": {"client_id": 1},
                },
                "create_new_client": {
                    "summary": "Create a new client from unresolved meeting",
                    "value": {"new_client_name": "Amit Verma"},
                },
            }
        ),
    ],
    db: AsyncSession = Depends(get_db),
) -> dict:
    try:
        result = await MeetingProcessingService().confirm_client(
            db,
            meeting_id=meeting_id,
            client_id=request.client_id,
            new_client_name=request.new_client_name,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found.")
    return result


@router.patch("/{meeting_id}/transcript", response_model=dict)
async def update_transcript(
    meeting_id: int,
    request: TranscriptUpdate,
    db: AsyncSession = Depends(get_db)
):
    from app.models.meeting import Meeting

    result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
    meeting = result.scalar_one_or_none()
    
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found.")
        
    meeting.raw_notes = request.raw_notes
    meeting.status = MeetingStatus.PROCESSING.value
    await db.commit()
    
    # TRIGGER ARQ BACKGROUND JOB
    pool = get_arq_pool()
    if pool:
        await pool.enqueue_job(
            "generate_meeting_embeddings",
            meeting.id,
            organization_id="default",
            user_id="default",
            _job_id=f"generate_meeting_embeddings_{meeting.id}"
        )
        
    return {"message": "Transcript updated successfully. Reprocessing queued.", "meeting_id": meeting.id}


@router.get("/{meeting_id}", response_model=dict)
async def get_meeting(meeting_id: int, db: AsyncSession = Depends(get_db)):
    """Fetch audio-processing status and its displayable result for polling."""
    from app.models.meeting import Meeting

    result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
    meeting = result.scalar_one_or_none()
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found.")

    # Audio processing is asynchronous.  Once it completes the browser needs
    # the same essentials it shows after a pasted-note request: summary and
    # the commitments linked to this meeting.
    from app.models.commitment import Commitment, CommitmentMeetingLink
    from app.services.json_utils import from_json

    commitments_result = await db.execute(
        select(Commitment)
        .join(
            CommitmentMeetingLink,
            CommitmentMeetingLink.commitment_id == Commitment.id,
        )
        .where(CommitmentMeetingLink.meeting_id == meeting.id)
    )
    commitments = commitments_result.scalars().all()

    return {
        "id": meeting.id,
        "status": meeting.status,
        "client_id": meeting.client_id,
        "client_identification_status": meeting.client_identification_status,
        "suggested_name": getattr(meeting, "suggested_client_name", ""),
        "summary": meeting.summary,
        "key_discussion_points": from_json(meeting.key_discussion_points_json, []),
        "concerns": from_json(meeting.concerns_json, []),
        "commitments": [
            {
                "id": commitment.id,
                "description": commitment.description,
                "owner": commitment.owner,
                "due_date": commitment.due_date.isoformat() if commitment.due_date else None,
                "due_date_text": commitment.due_date_text,
                "urgency_level": commitment.urgency_level,
                "status": commitment.status,
                "extraction_confidence": commitment.extraction_confidence,
            }
            for commitment in commitments
        ],
    }
