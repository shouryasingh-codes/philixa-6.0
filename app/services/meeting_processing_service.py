from __future__ import annotations

import json
import logging
from datetime import date
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.provider import AIExtractionError, AIProvider, get_ai_provider
from app.core.config import Settings, get_settings
from app.models.ai_extraction_log import AIExtractionLog
from app.models.client import Client
from app.models.meeting import Meeting
from app.schemas.meeting_note import MeetingNoteProcessRequest
from app.services.client_identification_service import ClientIdentificationService
from app.services.commitment_service import CommitmentService
from app.services.json_utils import from_json, to_json
from app.services.memory_service import MemoryService


logger = logging.getLogger(__name__)


class MeetingProcessingService:
    def __init__(
        self,
        settings: Settings | None = None,
        ai_provider: AIProvider | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.ai_provider = ai_provider or get_ai_provider(self.settings)
        self.client_identifier = ClientIdentificationService(self.settings)
        self.commitments = CommitmentService()
        self.memory = MemoryService()

    def process_notes(
        self, db: Session, request: MeetingNoteProcessRequest
    ) -> dict[str, Any]:
        meeting_date = request.meeting_date or date.today()
        try:
            extraction = self.ai_provider.extract_meeting_intelligence(
                request.raw_notes, meeting_date
            )
        except AIExtractionError:
            logger.exception("AI extraction failed.")
            raise
        except Exception as exc:
            logger.exception("Unexpected AI extraction failure.")
            raise AIExtractionError("Unexpected AI extraction failure.") from exc

        client_info = extraction.get("client_identification", {})
        client, client_status, warnings = self.client_identifier.resolve_client(
            db,
            suggested_name=client_info.get("suggested_client_name"),
            confidence=float(client_info.get("confidence") or 0.0),
            known_client_id=request.known_client_id,
        )
        warnings.extend(extraction.get("warnings") or [])
        meeting = Meeting(
            client_id=client.id if client else None,
            raw_notes=request.raw_notes,
            meeting_date=meeting_date,
            summary=extraction.get("meeting_summary") or "",
            key_discussion_points_json=to_json(extraction.get("key_discussion_points") or []),
            concerns_json=to_json(extraction.get("concerns") or []),
            status="processed" if client else "client_identification_required",
            client_identification_status=client_status,
            client_identification_confidence=float(client_info.get("confidence") or 0.0),
        )
        db.add(meeting)
        db.flush()
        db.add(
            AIExtractionLog(
                meeting_id=meeting.id,
                provider=self.ai_provider.provider_name,
                model=self.ai_provider.model_name,
                prompt_version=self.settings.prompt_version,
                raw_response_json=to_json(extraction),
                parsed_response_json=to_json(extraction),
                success=True,
            )
        )

        created = []
        updated = []
        if client:
            self._merge_client_products(client, extraction.get("products_owned") or [])
            created, updated = self.commitments.upsert_commitments(
                db,
                client_id=client.id,
                meeting_id=meeting.id,
                extracted_commitments=extraction.get("commitments") or [],
            )
            self.memory.update_client_memory(db, client.id)

        db.commit()
        return self._response_payload(
            db,
            meeting=meeting,
            client=client,
            client_status=client_status,
            extraction=extraction,
            created=created,
            updated=updated,
            warnings=warnings,
        )

    def confirm_client(
        self,
        db: Session,
        *,
        meeting_id: int,
        client_id: int | None = None,
        new_client_name: str | None = None,
    ) -> dict[str, Any] | None:
        meeting = db.get(Meeting, meeting_id)
        if not meeting:
            return None
        if client_id and new_client_name:
            raise ValueError("Provide either client_id or new_client_name, not both.")
        if client_id:
            client = db.get(Client, client_id)
            if not client:
                raise ValueError("Client not found.")
            client_status = "identified"
        elif new_client_name:
            client = Client(
                name=new_client_name,
                normalized_name=self._normalize_client_name(new_client_name),
            )
            db.add(client)
            db.flush()
            client_status = "created"
        else:
            raise ValueError("Either client_id or new_client_name is required.")

        latest_log = db.scalar(
            select(AIExtractionLog)
            .where(AIExtractionLog.meeting_id == meeting_id, AIExtractionLog.success.is_(True))
            .order_by(AIExtractionLog.created_at.desc())
        )
        extraction = from_json(latest_log.parsed_response_json if latest_log else "{}", {})
        meeting.client_id = client.id
        meeting.status = "processed"
        meeting.client_identification_status = client_status
        db.add(meeting)
        self._merge_client_products(client, extraction.get("products_owned") or [])
        created, updated = self.commitments.upsert_commitments(
            db,
            client_id=client.id,
            meeting_id=meeting.id,
            extracted_commitments=extraction.get("commitments") or [],
        )
        self.memory.update_client_memory(db, client.id)
        db.commit()
        return self._response_payload(
            db,
            meeting=meeting,
            client=client,
            client_status=client_status,
            extraction=extraction,
            created=created,
            updated=updated,
            warnings=[],
        )

    def _response_payload(
        self,
        db: Session,
        *,
        meeting: Meeting,
        client: Client | None,
        client_status: str,
        extraction: dict[str, Any],
        created: list,
        updated: list,
        warnings: list[str],
    ) -> dict[str, Any]:
        unique_warnings = list(dict.fromkeys(warnings))
        pending = self.commitments.pending_for_client(db, client.id) if client else []
        return {
            "meeting_id": meeting.id,
            "client_status": client_status,
            "client_id": client.id if client else None,
            "requires_client_confirmation": client is None,
            "meeting_summary": meeting.summary,
            "meeting": meeting_to_dict(meeting),
            "extraction": self._extraction_payload(
                extraction=extraction,
                client=client,
                client_status=client_status,
                warnings=unique_warnings,
            ),
            "commitments_created": created,
            "commitments_updated": updated,
            "pending_commitments": pending,
            "warnings": unique_warnings,
        }

    @staticmethod
    def _normalize_client_name(name: str) -> str:
        from app.utils.text_normalization import normalize_text

        return normalize_text(name)

    def _extraction_payload(
        self,
        *,
        extraction: dict[str, Any],
        client: Client | None,
        client_status: str,
        warnings: list[str],
    ) -> dict[str, Any]:
        client_identification = extraction.get("client_identification", {})
        extracted_commitments = [
            self._sanitize_extracted_commitment(item)
            for item in extraction.get("commitments") or []
            if item.get("description")
        ]
        return {
            "client_identification": {
                "status": client_status,
                "matched_client_id": client.id if client else client_identification.get("matched_client_id"),
                "suggested_client_name": (
                    client.name
                    if client
                    else client_identification.get("suggested_client_name")
                ),
                "confidence": float(client_identification.get("confidence") or 0.0),
                "requires_confirmation": client is None,
            },
            "meeting_summary": extraction.get("meeting_summary") or "",
            "key_discussion_points": extraction.get("key_discussion_points") or [],
            "products_owned": extraction.get("products_owned") or [],
            "concerns": extraction.get("concerns") or [],
            "commitments": extracted_commitments,
            "action_items": extraction.get("action_items")
            or [item["description"] for item in extracted_commitments],
            "warnings": warnings,
        }

    def _sanitize_extracted_commitment(self, item: dict[str, Any]) -> dict[str, Any]:
        due_date_confidence = float(item.get("due_date_confidence") or 0.0)
        due_date = item.get("due_date")
        if due_date_confidence < self.settings.due_date_threshold:
            due_date = None
        return {
            "description": item.get("description") or "",
            "owner": item.get("owner") or "RM",
            "due_date": due_date,
            "due_date_text": item.get("due_date_text"),
            "due_date_confidence": due_date_confidence,
            "urgency_level": item.get("urgency_level") or "medium",
            "status": item.get("status") or "pending",
            "confidence": float(item.get("confidence") or item.get("extraction_confidence") or 0.0),
        }

    def _merge_client_products(self, client: Client, products: list[str]) -> None:
        if not products:
            return
        existing = from_json(client.products_owned_json, [])
        merged: list[str] = []
        seen: set[str] = set()
        for value in [*existing, *products]:
            product = str(value or "").strip()
            if not product:
                continue
            key = product.casefold()
            if key in seen:
                continue
            seen.add(key)
            merged.append(product)
        client.products_owned_json = to_json(merged)


def meeting_to_dict(meeting: Meeting) -> dict[str, Any]:
    return {
        "id": meeting.id,
        "client_id": meeting.client_id,
        "raw_notes": meeting.raw_notes,
        "meeting_date": meeting.meeting_date.isoformat(),
        "summary": meeting.summary,
        "key_discussion_points": from_json(meeting.key_discussion_points_json, []),
        "concerns": from_json(meeting.concerns_json, []),
        "status": meeting.status,
        "client_identification_status": meeting.client_identification_status,
        "client_identification_confidence": meeting.client_identification_confidence,
    }
