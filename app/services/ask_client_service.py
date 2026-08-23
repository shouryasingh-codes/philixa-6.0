from __future__ import annotations

import asyncio
from datetime import date
import json
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.provider import get_ai_provider
from app.core.auth import Principal
from app.core.config import get_settings
from app.models.client import Client
from app.models.meeting import Meeting

logger = logging.getLogger(__name__)


class AskClientService:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def _parse_query(self, query: str) -> dict:
        today_str = date.today().isoformat()
        prompt = (
            f"You are a search query parser. Today's date is {today_str}.\n"
            f"Extract date ranges and exact keywords from the user's natural language query.\n"
            f"User query: '{query}'\n\n"
            f"Rules:\n"
            f"1. If the user mentions a specific timeline (e.g. 'last 6 months', '2023', 'last week'), calculate the start_date and end_date in YYYY-MM-DD format.\n"
            f"2. If no time is mentioned, leave start_date and end_date as null.\n"
            f"3. If the user mentions specific policy numbers, IDs, or exact names, put them in exact_keywords. Otherwise leave it empty.\n"
            f"4. optimized_query should be a clean version of the question for vector search.\n"
        )

        schema = {
            "type": "object",
            "properties": {
                "optimized_query": {"type": "string"},
                "start_date": {"type": ["string", "null"]},
                "end_date": {"type": ["string", "null"]},
                "exact_keywords": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "required": ["optimized_query", "start_date", "end_date", "exact_keywords"],
        }

        try:
            provider = get_ai_provider(self.settings.ai_economy_provider, self.settings)
            response_json = await asyncio.to_thread(
                provider.generate_json,
                model=self.settings.ai_economy_model,
                prompt=prompt,
                schema=schema,
            )
            return json.loads(response_json)
        except Exception as e:
            logger.error(f"Failed to parse query, falling back: {e}")
            return {
                "optimized_query": query,
                "start_date": None,
                "end_date": None,
                "exact_keywords": [],
            }

    async def ask(
        self,
        db: AsyncSession,
        client_id: int,
        query: str,
        principal: Principal | None = None,
    ) -> dict:
        if principal is not None:
            from app.repositories.client_repository import ClientRepository
            client = await ClientRepository().get_by_id(db, principal, client_id)
        else:
            client = await db.get(Client, client_id)

        if not client:
            raise ValueError("Client not found.")

        from app.services.semantic_search_service import search_meeting_evidence

        parsed = await self._parse_query(query)

        start_date = None
        end_date = None
        if parsed.get("start_date"):
            try:
                start_date = date.fromisoformat(parsed["start_date"])
            except ValueError:
                pass
        if parsed.get("end_date"):
            try:
                end_date = date.fromisoformat(parsed["end_date"])
            except ValueError:
                pass

        evidence_list = await search_meeting_evidence(
            db=db,
            query=parsed.get("optimized_query", query),
            organization_id=client.organization_id,
            user_id=client.user_id,
            client_id=client_id,
            limit=5,
            start_date=start_date,
            end_date=end_date,
            exact_keywords=parsed.get("exact_keywords", []),
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
                            "items": {"type": "integer"},
                        },
                    },
                    "required": ["answer", "source_meetings"],
                },
            )
            result = json.loads(response_json)
            return {
                "answer": result.get("answer", "I couldn't find an answer in the client's history."),
                "source_meetings": result.get("source_meetings", []),
            }
        except Exception as e:
            logger.error(f"Error querying AI for Ask Client: {e}")
            return {
                "answer": "Sorry, I encountered an error while processing your request.",
                "source_meetings": [],
            }
