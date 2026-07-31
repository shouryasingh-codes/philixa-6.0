from sqlalchemy.ext.asyncio import AsyncSession
import json
import logging
from sqlalchemy import select
from datetime import date

from app.core.config import get_settings
from app.models.client import Client
from app.models.meeting import Meeting
from app.ai.provider import get_ai_provider

logger = logging.getLogger(__name__)

class AskClientService:
    def __init__(self):
        self.settings = get_settings()

    async def ask(self, db: AsyncSession, client_id: int, query: str) -> dict:
        client = await db.get(Client, client_id)
        if not client:
            raise ValueError("Client not found.")

        from app.services.semantic_search_service import search_meeting_evidence
        
        # New Day 7 Semantic Search Engine
        # Instead of loading the last 20 meetings blindly, we only search for the most relevant paragraphs using AI vectors!
        evidence_list = await search_meeting_evidence(
            db=db,
            query=query,
            organization_id="default", # Default placeholder
            user_id="default",         # Default placeholder
            client_id=client_id,
            limit=5
        )

        context_blocks = []
        for evidence in evidence_list:
            context_blocks.append(
                f"--- Meeting ID: {evidence['meeting_id']} | Date: {evidence['meeting_date'].isoformat()} ---\n"
                f"Snippet: {evidence['chunk_text']}"
            )

        context_str = "\n\n".join(context_blocks)

        prompt = (
            f"You are a helpful assistant for a Relationship Manager. "
            f"Answer ONLY the following query about client '{client.name}' using the provided meeting data.\n"
            f"CRITICAL INSTRUCTION 1: If 'Meeting history' is empty, you MUST reply with EXACTLY: 'I don't have any semantic memory for this client yet. Please process a meeting first.'\n"
            f"CRITICAL INSTRUCTION 2: If the specific person, topic, or entity mentioned in the query is NOT found in the 'Meeting history', you MUST reply with 'I cannot find any information about that in the client's history.' DO NOT guess, DO NOT hallucinate, and DO NOT substitute names.\n"
            f"Query: {query}\n\n"
            f"Meeting history:\n{context_str}\n\n"
            f"Format your response as JSON with two keys:\n"
            f"- 'answer': string containing your detailed answer. YOU MUST cite the meeting dates explicitly in the text.\n"
            f"- 'source_meetings': list of integer IDs of the meetings you used to formulate the answer.\n"
        )

        try:
            provider = get_ai_provider(self.settings.ai_economy_provider, self.settings)
            response_json = provider.generate_json(
                model=self.settings.ai_economy_model,
                prompt=prompt,
                schema={
                    "type": "object",
                    "properties": {
                        "answer": {"type": "string"},
                        "source_meetings": {
                            "type": "array",
                            "items": {"type": "integer"}
                        }
                    },
                    "required": ["answer", "source_meetings"]
                }
            )
            result = json.loads(response_json)
            return {
                "answer": result.get("answer", "I couldn't find an answer in the client's history."),
                "source_meetings": result.get("source_meetings", [])
            }
        except Exception as e:
            logger.error(f"Error querying AI for Ask Client: {e}")
            return {
                "answer": "Sorry, I encountered an error while processing your request.",
                "source_meetings": []
            }
