from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_api_key
from app.database.session import get_db
from app.models.ai_extraction_log import AIExtractionLog
from app.models.client import Client
from app.models.commitment import Commitment, CommitmentMeetingLink
from app.models.meeting import Meeting
from app.models.risk_signal import RiskSignal
from app.models.follow_up_task import FollowUpTask
from app.schemas.client import ClientListItem, ClientMemoryResponse, MeetingRead
from app.services.json_utils import from_json
from app.services.meeting_processing_service import meeting_to_dict
from app.services.memory_service import MemoryService
from app.schemas.ask_client import AskClientRequest, AskClientResponse
from app.services.ask_client_service import AskClientService

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", response_model=list[ClientListItem])
async def list_clients(db: AsyncSession = Depends(get_db)) -> list[dict]:
    clients_res = await db.scalars(select(Client).order_by(Client.updated_at.desc()))
    clients = list(clients_res.all())
    rows = []
    for client in clients:
        pending_count = await db.scalar(
            select(func.count(Commitment.id)).where(
                Commitment.client_id == client.id,
                Commitment.status == "pending",
            )
        )
        last_meeting = await db.scalar(
            select(Meeting)
            .where(Meeting.client_id == client.id)
            .order_by(Meeting.meeting_date.desc(), Meeting.created_at.desc())
            .limit(1)
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
async def get_client_memory(client_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    try:
        return await MemoryService().get_client_memory(db, client_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/{client_id}/ask", response_model=AskClientResponse)
async def ask_client(
    client_id: int,
    request: AskClientRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    try:
        return await AskClientService().ask(db, client_id, request.query)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{client_id}/meetings", response_model=list[MeetingRead])
async def get_client_meetings(client_id: int, db: AsyncSession = Depends(get_db)) -> list[dict]:
    client = await db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")
    meetings_res = await db.scalars(
        select(Meeting)
        .where(Meeting.client_id == client_id)
        .order_by(Meeting.meeting_date.desc(), Meeting.created_at.desc())
    )
    meetings = list(meetings_res.all())
    return [meeting_to_dict(meeting) for meeting in meetings]


@router.delete("/{client_id}")
async def delete_client(client_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    client = await db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")

    meeting_ids_res = await db.scalars(select(Meeting.id).where(Meeting.client_id == client_id))
    meeting_ids = list(meeting_ids_res.all())
    
    commitment_ids_res = await db.scalars(select(Commitment.id).where(Commitment.client_id == client_id))
    commitment_ids = list(commitment_ids_res.all())
    
    deleted_counts = {
        "client_id": client_id,
        "meetings_deleted": len(meeting_ids),
        "commitments_deleted": len(commitment_ids),
    }

    if commitment_ids or meeting_ids:
        if commitment_ids:
            await db.execute(
                delete(CommitmentMeetingLink).where(
                    CommitmentMeetingLink.commitment_id.in_(commitment_ids)
                )
            )
        if meeting_ids:
            await db.execute(
                delete(CommitmentMeetingLink).where(
                    CommitmentMeetingLink.meeting_id.in_(meeting_ids)
                )
            )
    # Delete RiskSignal and FollowUpTask attached to this client (Day 4 additions)
    await db.execute(delete(RiskSignal).where(RiskSignal.client_id == client_id))
    await db.execute(delete(FollowUpTask).where(FollowUpTask.client_id == client_id))

    if meeting_ids:
        await db.execute(delete(AIExtractionLog).where(AIExtractionLog.meeting_id.in_(meeting_ids)))
        await db.execute(delete(Meeting).where(Meeting.id.in_(meeting_ids)))
    if commitment_ids:
        await db.execute(delete(Commitment).where(Commitment.id.in_(commitment_ids)))

    await db.delete(client)
    await db.commit()
    return deleted_counts
