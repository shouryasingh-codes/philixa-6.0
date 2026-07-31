import logging
import asyncio
from arq import Retry
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.models.meeting import Meeting
from app.models.meeting_evidence import MeetingEvidence
from app.services.embedding_service import generate_embeddings_for_text

logger = logging.getLogger(__name__)

async def generate_meeting_embeddings(ctx: dict, meeting_id: int, organization_id: str = "default", user_id: str = "default") -> bool:
    """
    ARQ Background job to generate and save pgvector embeddings for a meeting.
    This job runs in the background and does not block the main FastAPI server.
    """
    logger.info(f"Starting embedding generation for meeting {meeting_id}")
    
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
            
        if not meeting.raw_notes:
            logger.info(f"Meeting {meeting_id} has no notes to embed")
            return True
            
        try:
            # We run the embedding function (CPU bound) in a threadpool
            # to ensure the async loop is never blocked, guaranteeing zero crashes.
            chunks = await asyncio.to_thread(generate_embeddings_for_text, meeting.raw_notes)
            
            # Delete any existing evidence chunks for this meeting to ensure idempotency
            delete_stmt = delete(MeetingEvidence).where(MeetingEvidence.meeting_id == meeting.id)
            await db.execute(delete_stmt)
            
            # Create evidence models
            evidence_objects = []
            for chunk in chunks:
                evidence = MeetingEvidence(
                    meeting_id=meeting.id,
                    organization_id=organization_id,
                    user_id=user_id,
                    chunk_index=chunk["chunk_index"],
                    chunk_text=chunk["chunk_text"],
                    embedding=chunk["embedding"]
                )
                evidence_objects.append(evidence)
                
            if evidence_objects:
                db.add_all(evidence_objects)
                await db.commit()
                logger.info(f"Successfully saved {len(evidence_objects)} embedded chunks for meeting {meeting_id}")
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate embeddings for meeting {meeting_id}: {str(e)}")
            await db.rollback()
            raise Retry(defer=60) # Automatically retry after 60s if failure occurs
