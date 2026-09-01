from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Tuple
from fastapi import BackgroundTasks
from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.provider import get_ai_provider
from app.core.auth import Principal
from app.core.config import Settings
from app.models.client import Client
from app.models.meeting import Meeting
from app.database.session import AsyncSessionLocal
from app.services.meeting_processing_service import MeetingProcessingService
from app.services.portfolio_copilot_service import process_copilot_query
from app.schemas.meeting_note import MeetingNoteProcessRequest

logger = logging.getLogger(__name__)


class VoiceAssistantService:
    def __init__(self, db: AsyncSession, settings: Settings) -> None:
        self.db = db
        self.settings = settings

        self.economy_provider = get_ai_provider(self.settings.ai_economy_provider, self.settings)
        self.economy_model = self.settings.ai_economy_model

        self.review_provider = get_ai_provider(self.settings.ai_review_provider, self.settings)
        self.review_model = self.settings.ai_review_model

    async def chat(
        self,
        user_text: str,
        conversation_history: List[Dict[str, str]] | None = None,
        principal: Principal | None = None,
        background_tasks: BackgroundTasks | None = None,
    ) -> Tuple[str, Optional[int]]:
        """
        Process user's voice transcript and return a conversational response.
        """
        if conversation_history is None:
            conversation_history = []

        logger.info(f"Voice Assistant received: '{user_text}'")

        # Step 1: Extract Entities and Intent
        intent_schema = {
            "intent": "string (either 'QUERY', 'SAVE_MEETING', or 'GENERAL_CHAT')",
            "client_name": "string (extracted client name, or null if none)",
            "meeting_notes": "string (the notes to save, if intent is SAVE_MEETING, else null)",
        }

        transcript = user_text

        try:
            intent_json_str = await asyncio.to_thread(
                self.economy_provider.generate_json,
                self.economy_model,
                f"User just said: '{transcript}'.\nAnalyze the user's voice input (which might be in Hindi/Hinglish) and extract intent. If they are talking about a client meeting to save, return SAVE_MEETING. If they are asking a question about a specific person, client, past discussion, or ANY portfolio metrics/data (like 'how many meetings', 'who asked for discount'), return QUERY and extract the person's name if applicable (TRANSLATE AND SPELL HINDI NAMES IN ENGLISH, e.g. 'मनोज' -> 'Manoj'). Otherwise, return GENERAL_CHAT.",
                json.loads(json.dumps(intent_schema)),
            )
            intent_data = json.loads(intent_json_str)
        except Exception as e_econ:
            logger.warning(f"Economy intent extraction failed: {e_econ}. Falling back to Review model.")
            try:
                intent_json_str = await asyncio.to_thread(
                    self.review_provider.generate_json,
                    self.review_model,
                    f"User just said: '{transcript}'.\nAnalyze the user's voice input (which might be in Hindi/Hinglish) and extract intent. If they are talking about a client meeting to save, return SAVE_MEETING. If they are asking a question about a specific person, client, past discussion, or ANY portfolio metrics/data (like 'how many meetings', 'who asked for discount'), return QUERY and extract the person's name if applicable (TRANSLATE AND SPELL HINDI NAMES IN ENGLISH, e.g. 'मनोज' -> 'Manoj'). Otherwise, return GENERAL_CHAT.",
                    json.loads(json.dumps(intent_schema)),
                )
                intent_data = json.loads(intent_json_str)
            except Exception as e_rev:
                logger.error(f"Review intent extraction also failed: {e_rev}")
                intent_data = {"intent": "GENERAL_CHAT", "client_name": None}

        intent = intent_data.get("intent", "GENERAL_CHAT")
        client_name = intent_data.get("client_name")

        logger.info(f"Voice Assistant Intent: {intent}, Client: {client_name}")

        # Step 2: Context Retrieval (Memory)
        memory_context = ""
        client = None

        if intent == "QUERY" and principal:
            try:
                copilot_result = await process_copilot_query(
                    user_text,
                    principal.organization_id,
                    principal.user_id,
                    principal.role,
                    self.db,
                )
                memory_context = f"The database search returned this precise answer: {copilot_result['answer']}"
            except Exception as e:
                logger.warning(f"Portfolio Copilot query failed for voice assistant: {e}")
                memory_context = "Could not retrieve portfolio data due to an error."
        elif client_name and intent == "SAVE_MEETING":
            try:
                client_stmt = select(Client).where(Client.name.ilike(f"%{client_name}%"))
                if principal is not None:
                    client_stmt = client_stmt.where(Client.organization_id == principal.organization_id)
                    if principal.role.lower() == "member":
                        client_stmt = client_stmt.where(Client.user_id == principal.user_id)
                client_stmt = client_stmt.limit(1)

                client_res = await self.db.execute(client_stmt)
                client = client_res.scalar_one_or_none()

                if client:
                    meeting_stmt = select(Meeting).where(
                        Meeting.client_id == client.id,
                        Meeting.organization_id == client.organization_id,
                    )
                    if principal is not None and principal.role.lower() == "member":
                        meeting_stmt = meeting_stmt.where(Meeting.user_id == principal.user_id)
                    meeting_stmt = meeting_stmt.order_by(Meeting.meeting_date.desc()).limit(3)

                    meeting_res = await self.db.execute(meeting_stmt)
                    meetings = meeting_res.scalars().all()

                    if meetings:
                        memory_context = f"Here is the context from the database regarding PAST meetings for {client.name} (These meetings have ALREADY happened):\n"
                        for m in meetings:
                            memory_context += f"- Past meeting that occurred on {m.meeting_date}: {m.summary}\n"
                    else:
                        memory_context = f"Found client {client.name} but no previous meetings recorded."
                else:
                    memory_context = f"No previous records found for {client_name}."
            except Exception as e:
                logger.warning(f"Semantic search failed for voice assistant: {e}")
                memory_context = "Could not retrieve past records due to an error."

        # Trigger Background Save for Meetings
        meeting_id = None
        if intent == "SAVE_MEETING" and intent_data.get("meeting_notes") and principal:
            notes_to_save = intent_data.get("meeting_notes")
            resolved_client_id = client.id if client else None
            
            # Synchronously create the Meeting row to get the ID
            meeting = Meeting(
                organization_id=principal.organization_id,
                user_id=principal.user_id,
                client_id=None,
                raw_notes=notes_to_save,
                meeting_date=date.today(),
                source_type="voice",
                summary="",
                key_discussion_points_json="[]",
                concerns_json="[]",
                status="manual_review_required",
                client_identification_status="unknown",
                client_identification_confidence=0.0,
            )
            self.db.add(meeting)
            await self.db.flush()
            meeting_id = meeting.id
            await self.db.commit() # Important: Commit so the background task can query it
            
            async def background_save(m_id):
                async with AsyncSessionLocal() as bg_db:
                    try:
                        # Fetch the meeting we just created
                        m_res = await bg_db.execute(select(Meeting).where(Meeting.id == m_id))
                        m = m_res.scalar_one_or_none()
                        if m:
                            svc = MeetingProcessingService(self.settings, self.economy_provider)
                            await svc.process_existing_meeting(bg_db, m, resolved_client_id)
                    except Exception as e:
                        logger.error(f"Voice background save failed for meeting {m_id}: {e}")

            if background_tasks:
                background_tasks.add_task(background_save, meeting_id)
            else:
                asyncio.create_task(background_save(meeting_id))
            
            memory_context += "\n\nSYSTEM INSTRUCTION: You have successfully started saving the meeting notes in the background. Tell the user exactly this: 'Okay, I am saving this meeting for you now.'"

        # Step 3: Generate Conversational Response
        system_prompt = (
            "You are Philixa, an energetic and smart AI voice assistant for insurance agents. "
            "You have a confident, conversational, and direct personality. "
            "IMPORTANT: Keep your answers VERY short (1-2 sentences). You are speaking aloud, so don't use bullet points, markdown, or complex words. "
            "CRITICAL RULE: If the user asks about a specific person or topic and you DO NOT see their details in the 'Context from database', you MUST reply saying you don't have information about them. DO NOT make up or hallucinate details. "
            "NOTE: You may reply in Hinglish (a natural mix of Hindi and English) if the user speaks in Hinglish. "
            f"Context from database: {memory_context}"
        )

        if memory_context:
            system_prompt += f"\n\nDATABASE CONTEXT:\n{memory_context}"

        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-4:]])

        final_user_prompt = ""
        if history_text:
            final_user_prompt += f"Recent Conversation:\n{history_text}\n\n"
        final_user_prompt += f"Manager: {user_text}"

        try:
            response_text = await asyncio.to_thread(
                self.economy_provider.generate_text,
                self.economy_model,
                system_prompt,
                final_user_prompt,
            )
        except Exception as e_econ:
            logger.warning(f"Economy voice generation failed: {e_econ}. Falling back to Review model.")
            try:
                response_text = await asyncio.to_thread(
                    self.review_provider.generate_text,
                    self.review_model,
                    system_prompt,
                    final_user_prompt,
                )
            except Exception as e:
                logger.error(f"LLM Generation error: {e}")
                return "I'm having trouble processing that right now.", meeting_id

        return response_text, meeting_id
