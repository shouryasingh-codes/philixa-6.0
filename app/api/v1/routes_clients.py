from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.core.security import require_api_key
from app.database.session import get_db
from app.models.ai_extraction_log import AIExtractionLog
from app.models.client import Client
from app.models.commitment import Commitment, CommitmentMeetingLink
from app.models.meeting import Meeting
from app.schemas.client import ClientListItem, ClientMemoryResponse, MeetingRead
from app.services.json_utils import from_json
from app.services.meeting_processing_service import meeting_to_dict
from app.services.memory_service import MemoryService


router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", response_model=list[ClientListItem])
def list_clients(db: Session = Depends(get_db)) -> list[dict]:
    clients = list(db.scalars(select(Client).order_by(Client.updated_at.desc())).all())
    rows = []
    for client in clients:
        pending_count = db.scalar(
            select(func.count(Commitment.id)).where(
                Commitment.client_id == client.id,
                Commitment.status == "pending",
            )
        )
        last_meeting = db.scalar(
            select(Meeting)
            .where(Meeting.client_id == client.id)
            .order_by(Meeting.meeting_date.desc(), Meeting.created_at.desc())
        )
        rows.append(
            {
                "id": client.id,
                "name": client.name,
                "products_owned": from_json(client.products_owned_json, []),
                "rolling_summary": client.rolling_summary,
                "pending_commitments_count": int(pending_count or 0),
                "last_meeting_summary": last_meeting.summary if last_meeting else None,
                "created_at": client.created_at,
                "updated_at": client.updated_at,
            }
        )
    return rows


@router.get("/{client_id}/memory", response_model=ClientMemoryResponse)
def get_client_memory(client_id: int, db: Session = Depends(get_db)) -> dict:
    try:
        return MemoryService().get_client_memory(db, client_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{client_id}/meetings", response_model=list[MeetingRead])
def get_client_meetings(client_id: int, db: Session = Depends(get_db)) -> list[dict]:
    if not db.get(Client, client_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")
    meetings = list(
        db.scalars(
            select(Meeting)
            .where(Meeting.client_id == client_id)
            .order_by(Meeting.meeting_date.desc(), Meeting.created_at.desc())
        ).all()
    )
    return [meeting_to_dict(meeting) for meeting in meetings]


@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)) -> dict:
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")

    meeting_ids = list(db.scalars(select(Meeting.id).where(Meeting.client_id == client_id)))
    commitment_ids = list(
        db.scalars(select(Commitment.id).where(Commitment.client_id == client_id))
    )
    deleted_counts = {
        "client_id": client_id,
        "meetings_deleted": len(meeting_ids),
        "commitments_deleted": len(commitment_ids),
    }

    if commitment_ids:
        db.execute(
            delete(CommitmentMeetingLink).where(
                CommitmentMeetingLink.commitment_id.in_(commitment_ids)
            )
        )
    if meeting_ids:
        db.execute(
            delete(CommitmentMeetingLink).where(
                CommitmentMeetingLink.meeting_id.in_(meeting_ids)
            )
        )
        db.execute(delete(AIExtractionLog).where(AIExtractionLog.meeting_id.in_(meeting_ids)))
        db.execute(delete(Meeting).where(Meeting.id.in_(meeting_ids)))
    if commitment_ids:
        db.execute(delete(Commitment).where(Commitment.id.in_(commitment_ids)))

    db.delete(client)
    db.commit()
    return deleted_counts
