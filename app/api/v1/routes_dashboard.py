from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

from app.core.security import get_current_org_id
from app.database.session import get_db
from app.models.client import Client
from app.models.follow_up_task import FollowUpTask
from app.models.risk_signal import RiskSignal
from app.schemas.dashboard import DailyPrioritiesResponse, FollowUpTaskRead, RiskSignalRead

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    dependencies=[Depends(get_current_org_id)],
)

@router.get("/priorities", response_model=DailyPrioritiesResponse)
async def get_daily_priorities(
    db: AsyncSession = Depends(get_db),
    org_id: str = Depends(get_current_org_id),
):
    today = date.today()

    # Derive date-sensitive flags at read time so this GET remains side-effect
    # free while still surfacing tasks that became overdue overnight.
    owned_client_ids_subq = (
        select(Client.id).scalar_subquery()
    )
    # P1 Bug 1 fix: scope tasks and risks to the current org only
    tasks = (await db.scalars(
        select(FollowUpTask)
        .options(selectinload(FollowUpTask.client))
        .where(
            FollowUpTask.client_id.in_(owned_client_ids_subq),
            FollowUpTask.is_completed == False,  # noqa: E712
            or_(FollowUpTask.due_date == today, FollowUpTask.due_date < today),
        )
        .order_by(FollowUpTask.due_date.asc())
    )).all()
    
    risks = (await db.scalars(
        select(RiskSignal)
        .options(selectinload(RiskSignal.client))
        .where(
            RiskSignal.client_id.in_(owned_client_ids_subq),
            or_(RiskSignal.is_high_risk == True, RiskSignal.requires_review == True),  # noqa: E712
        )
        .order_by(RiskSignal.confidence.desc())
    )).all()

    task_reads = [
        FollowUpTaskRead(
            id=t.id,
            client_id=t.client_id,
            client_name=t.client.name if t.client else None,
            commitment_id=t.commitment_id,
            description=t.description,
            due_date=t.due_date,
            is_completed=t.is_completed,
            is_overdue=bool(t.due_date and t.due_date < today),
            is_due_today=bool(t.due_date and t.due_date == today)
        ) for t in tasks
    ]

    risk_reads = [
        RiskSignalRead(
            id=r.id,
            client_id=r.client_id,
            client_name=r.client.name if r.client else None,
            meeting_id=r.meeting_id,
            description=r.description,
            severity_level=r.severity_level,
            confidence=r.confidence,
            is_high_risk=r.is_high_risk,
            requires_review=r.requires_review
        ) for r in risks
    ]

    return DailyPrioritiesResponse(tasks=task_reads, risks=risk_reads)
