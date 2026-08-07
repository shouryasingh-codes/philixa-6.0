import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.meeting_evidence import MeetingEvidence
from app.models.meeting import Meeting
from app.services.embedding_service import generate_query_embedding
from datetime import date

logger = logging.getLogger(__name__)

async def search_meeting_evidence(
    db: AsyncSession,
    query: str,
    organization_id: str,
    user_id: str,
    client_id: int | None = None,
    limit: int = 5,
    start_date: date | None = None,
    end_date: date | None = None,
    exact_keywords: list[str] | None = None
) -> list[dict]:
    """
    Hybrid retrieval: Semantic search + SQL keyword/tenant/date filters.
    """
    # 1. Generate query embedding (uses 'query: ' prefix internally)
    query_vector = generate_query_embedding(query)
    
    # 2. Build the query with mandatory tenant isolation filters
    stmt = (
        select(MeetingEvidence, Meeting)
        .join(Meeting, MeetingEvidence.meeting_id == Meeting.id)
        .where(MeetingEvidence.organization_id == organization_id)
        .where(MeetingEvidence.user_id == user_id)
    )
    
    # Apply optional client filter
    if client_id:
        stmt = stmt.where(Meeting.client_id == client_id)
        
    # Apply Date filters
    if start_date:
        stmt = stmt.where(Meeting.meeting_date >= start_date)
    if end_date:
        stmt = stmt.where(Meeting.meeting_date <= end_date)
        
    # Apply Keyword filters (DISABLED: breaks semantic search if words are not verbatim in chunk)
    # if exact_keywords:
    #     for kw in exact_keywords:
    #         if kw and kw.strip():
    #             stmt = stmt.where(MeetingEvidence.chunk_text.ilike(f"%{kw.strip()}%"))
        
    # 3. Apply pgvector semantic search
    # Order by cosine distance (<=> operator in Postgres)
    stmt = stmt.order_by(MeetingEvidence.embedding.cosine_distance(query_vector)).limit(limit)
    
    result = await db.execute(stmt)
    rows = result.all()
    
    # 4. Format results safely with evidence snippets
    evidence_list = []
    for evidence, meeting in rows:
        evidence_list.append({
            "meeting_id": meeting.id,
            "meeting_date": meeting.meeting_date,
            "source_type": meeting.source_type,
            "chunk_text": evidence.chunk_text
        })
        
    return evidence_list
