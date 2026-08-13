import logging
import json
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import Settings
from app.ai.provider import get_ai_provider
from sqlalchemy import select
from app.models.client import Client
from app.models.meeting import Meeting

logger = logging.getLogger(__name__)

class VoiceAssistantService:
    def __init__(self, db: AsyncSession, settings: Settings):
        self.db = db
        self.settings = settings
        
        # We set up BOTH providers for the Day 3 Safe Retry / Fallback logic
        self.economy_provider = get_ai_provider(self.settings.ai_economy_provider, self.settings)
        self.economy_model = self.settings.ai_economy_model
        
        self.review_provider = get_ai_provider(self.settings.ai_review_provider, self.settings)
        self.review_model = self.settings.ai_review_model

    async def chat(self, user_text: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Process user's voice transcript and return a conversational response.
        """
        if conversation_history is None:
            conversation_history = []
            
        logger.info(f"Voice Assistant received: '{user_text}'")

        # Step 1: Extract Entities and Intent
        # We need to know if the user is asking about a specific client.
        intent_schema = {
            "intent": "string (either 'QUERY', 'SAVE_MEETING', or 'GENERAL_CHAT')",
            "client_name": "string (extracted client name, or null if none)",
            "meeting_notes": "string (the notes to save, if intent is SAVE_MEETING, else null)"
        }
        
        extraction_prompt = (
            f"User just said: '{user_text}'.\n"
            f"Analyze the intent. Is the user asking a question about a client (QUERY)? "
            f"Are they dictating a meeting to be saved (SAVE_MEETING)? "
            f"Or is it just general conversation (GENERAL_CHAT)?"
        )
        
        transcript = user_text
        
        try:
            import asyncio
            intent_json_str = await asyncio.to_thread(
                self.economy_provider.generate_json,
                self.economy_model,
                f"User just said: '{transcript}'.\nAnalyze the user's voice input (which might be in Hindi/Hinglish) and extract intent. If they are talking about a client meeting to save, return SAVE_MEETING. If they are asking a question about a specific person, client, or past discussion (even if the word 'client' isn't explicitly used), return QUERY and extract the person's name (TRANSLATE AND SPELL HINDI NAMES IN ENGLISH, e.g. 'मनोज' -> 'Manoj'). Otherwise, return GENERAL_CHAT.",
                json.loads(json.dumps(intent_schema))
            )
            intent_data = json.loads(intent_json_str)
        except Exception as e_econ:
            logger.warning(f"Economy intent extraction failed: {e_econ}. Falling back to Review model.")
            try:
                intent_json_str = await asyncio.to_thread(
                    self.review_provider.generate_json,
                    self.review_model,
                    f"User just said: '{transcript}'.\nAnalyze the user's voice input (which might be in Hindi/Hinglish) and extract intent. If they are talking about a client meeting to save, return SAVE_MEETING. If they are asking a question about a specific person, client, or past discussion (even if the word 'client' isn't explicitly used), return QUERY and extract the person's name (TRANSLATE AND SPELL HINDI NAMES IN ENGLISH, e.g. 'मनोज' -> 'Manoj'). Otherwise, return GENERAL_CHAT.",
                    json.loads(json.dumps(intent_schema))
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
        if client_name and intent in ["QUERY", "SAVE_MEETING"]:
            # Retrieve past meetings related to this client
            try:
                # Query DB for client and get recent meetings
                client_stmt = select(Client).where(Client.name.ilike(f"%{client_name}%")).limit(1)
                client_res = await self.db.execute(client_stmt)
                client = client_res.scalar_one_or_none()
                
                if client:
                    meeting_stmt = select(Meeting).where(Meeting.client_id == client.id).order_by(Meeting.meeting_date.desc()).limit(3)
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

        # Combine history with the new prompt
        # We just format history into the user prompt for simplicity in this V1
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-4:]])
        
        final_user_prompt = ""
        if history_text:
            final_user_prompt += f"Recent Conversation:\n{history_text}\n\n"
        final_user_prompt += f"Manager: {user_text}"

        try:
            import asyncio
            response_text = await asyncio.to_thread(
                self.economy_provider.generate_text,
                self.economy_model,
                system_prompt,
                transcript
            )
        except Exception as e_econ:
            logger.warning(f"Economy voice generation failed: {e_econ}. Falling back to Review model.")
            try:
                response_text = await asyncio.to_thread(
                    self.review_provider.generate_text,
                    self.review_model,
                    system_prompt,
                    transcript
                )
            except Exception as e_rev:
                logger.error(f"Review voice generation also failed: {e_rev}")
                return "Sorry, my brain disconnected for a second. Let's try that again."
        
        return response_text
