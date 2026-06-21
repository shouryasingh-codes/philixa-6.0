from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Commitment(Base):
    __tablename__ = "commitments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    normalized_description: Mapped[str] = mapped_column(String(520), nullable=False, index=True)
    owner: Mapped[str] = mapped_column(String(80), default="RM", nullable=False)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    due_date_text: Mapped[str | None] = mapped_column(String(120), nullable=True)
    due_date_confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    urgency_level: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="pending", nullable=False, index=True)
    extraction_confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )

    client = relationship("Client", back_populates="commitments")
    meeting_links = relationship("CommitmentMeetingLink", back_populates="commitment")


class CommitmentMeetingLink(Base):
    __tablename__ = "commitment_meeting_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    commitment_id: Mapped[int] = mapped_column(
        ForeignKey("commitments.id"), nullable=False, index=True
    )
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    commitment = relationship("Commitment", back_populates="meeting_links")
    meeting = relationship("Meeting", back_populates="commitment_links")
