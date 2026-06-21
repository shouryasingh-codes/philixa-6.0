from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

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


router = APIRouter(
    prefix="/meeting-notes",
    tags=["meeting notes"],
    dependencies=[Depends(require_api_key)],
)


@router.post("/process", response_model=MeetingNoteProcessResponse)
def process_meeting_note(
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
    db: Session = Depends(get_db),
) -> dict:
    try:
        return MeetingProcessingService().process_notes(db, request)
    except AIExtractionError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc


@router.post("/{meeting_id}/confirm-client", response_model=ClientConfirmationResponse)
def confirm_client(
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
    db: Session = Depends(get_db),
) -> dict:
    try:
        result = MeetingProcessingService().confirm_client(
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
