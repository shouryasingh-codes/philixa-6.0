from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    client_id: Mapped[int | None] = mapped_column(ForeignKey("clients.id"), nullable=True)
    raw_notes: Mapped[str] = mapped_column(Text, nullable=False)
    meeting_date: Mapped[date] = mapped_column(Date, nullable=False)
    summary: Mapped[str] = mapped_column(Text, default="", nullable=False)
    key_discussion_points_json: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    concerns_json: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="processed", nullable=False)
    client_identification_status: Mapped[str] = mapped_column(
        String(60), default="identified", nullable=False
    )
    client_identification_confidence: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )

    client = relationship("Client", back_populates="meetings")
    commitment_links = relationship("CommitmentMeetingLink", back_populates="meeting")
    ai_logs = relationship("AIExtractionLog", back_populates="meeting")
