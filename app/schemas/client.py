from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.common import CommitmentRead, ConcernRead


class ClientListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    products_owned: list[str]
    rolling_summary: str
    pending_commitments_count: int
    last_meeting_summary: str | None
    created_at: datetime
    updated_at: datetime


class PreMeetingBriefResponse(BaseModel):
    title: str
    products_owned: list[str]
    last_meeting: str
    pending: list[str]
    concern: str
    highest_urgency: str
    suggested_talking_point: str


class ClientMemoryResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "client_id": 1,
                "client_name": "Rajesh Sharma",
                "last_meeting_summary": "Rajesh Sharma discussed interest in a business loan and raised concern about processing time.",
                "pre_meeting_brief": {
                    "title": "Client Brief",
                    "products_owned": ["Business Loan"],
                    "last_meeting": "Business Loan Discussion",
                    "pending": ["Send documents by Friday"],
                    "concern": "Processing time",
                    "highest_urgency": "medium",
                    "suggested_talking_point": "Explain loan processing timeline.",
                },
                "products_owned": ["Business Loan"],
                "pending_commitments": [],
                "major_concerns": [
                    {
                        "description": "Processing time concern",
                        "severity": "medium",
                        "confidence": 0.86,
                    }
                ],
                "recent_relationship_notes": [
                    "Rajesh Sharma discussed interest in a business loan and raised concern about processing time."
                ],
                "rolling_summary": "Rajesh Sharma discussed a business loan and expressed concerns about processing timelines. One follow-up commitment is still open: send documents by Friday.",
            }
        }
    )

    client_id: int
    client_name: str
    last_meeting_summary: str
    pre_meeting_brief: "PreMeetingBriefResponse"
    products_owned: list[str]
    pending_commitments: list[CommitmentRead]
    major_concerns: list[ConcernRead]
    recent_relationship_notes: list[str]
    rolling_summary: str


class MeetingRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "client_id": 1,
                "raw_notes": "Met Rajesh Sharma today. Promised documents by Friday.",
                "meeting_date": "2026-06-19",
                "summary": "Rajesh Sharma discussed interest in a business loan and raised concern about processing time.",
                "key_discussion_points": [
                    "Interested in business loan",
                    "Concerned about loan processing time",
                ],
                "concerns": [
                    {
                        "description": "Processing time concern",
                        "severity": "medium",
                        "confidence": 0.86,
                    }
                ],
                "status": "processed",
                "client_identification_status": "identified",
                "client_identification_confidence": 0.92,
            }
        },
    )

    id: int
    client_id: int | None
    raw_notes: str
    meeting_date: str
    summary: str
    key_discussion_points: list[str]
    concerns: list[dict]
    status: str
    client_identification_status: str
    client_identification_confidence: float
