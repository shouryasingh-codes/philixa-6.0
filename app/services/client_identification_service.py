from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.models.client import Client
from app.utils.text_normalization import normalize_text, similarity


class ClientIdentificationService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def resolve_client(
        self,
        db: Session,
        suggested_name: str | None,
        confidence: float,
        known_client_id: int | None = None,
    ) -> tuple[Client | None, str, list[str]]:
        warnings: list[str] = []
        if known_client_id:
            client = db.get(Client, known_client_id)
            if not client:
                warnings.append("Known client id was not found.")
                return None, "client_identification_required", warnings
            return client, "identified", warnings

        if not suggested_name:
            warnings.append("Client identification required.")
            return None, "client_identification_required", warnings

        normalized = normalize_text(suggested_name)
        clients = list(db.scalars(select(Client)).all())
        exact = [client for client in clients if client.normalized_name == normalized]
        if exact and confidence >= self.settings.client_auto_match_threshold:
            return exact[0], "identified", warnings

        close_matches = [
            client
            for client in clients
            if similarity(client.normalized_name, normalized) >= self.settings.client_auto_match_threshold
        ]
        if len(close_matches) == 1 and confidence >= self.settings.client_auto_match_threshold:
            return close_matches[0], "identified", warnings
        if len(close_matches) > 1:
            warnings.append("Multiple similar clients found; confirmation required.")
            return None, "client_identification_required", warnings

        if confidence >= self.settings.client_auto_create_threshold:
            client = Client(name=suggested_name, normalized_name=normalized)
            db.add(client)
            db.flush()
            return client, "created", warnings

        warnings.append("Client confidence below auto-create threshold.")
        return None, "client_identification_required", warnings
