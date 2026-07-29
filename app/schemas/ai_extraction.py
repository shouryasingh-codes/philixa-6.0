from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskSignal(BaseModel):
    """
    Represents a client concern, risk, or negative sentiment extracted from the meeting.
    """
    description: str = Field(
        ..., 
        min_length=3, 
        max_length=500,
        description="Clear, concise description of the risk or concern."
    )
    severity: SeverityLevel = Field(
        ..., 
        description="Severity level of the risk. Must be exactly one of the enum values."
    )
    confidence: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="AI confidence score between 0.0 and 1.0."
    )
    # Made Optional — Gemini aur local provider dono kabhi nahi bhejte isko
    source_evidence: Optional[str] = Field(
        default=None,
        description="The exact snippet or quote from the raw transcript that proves this risk exists."
    )


class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CommitmentExtraction(BaseModel):
    """
    Represents a task, promise, or action item extracted from the meeting.
    """
    description: str = Field(
        ..., 
        min_length=3,
        description="Clear description of the promise or action item."
    )
    owner: str = Field(
        default="RM", 
        description="Who is responsible (e.g., 'RM', 'Client', 'Operations')."
    )
    due_date: Optional[date] = Field(
        default=None, 
        description="Exact due date IF AND ONLY IF clearly mentioned. If ambiguous or unclear (e.g. 'soon', 'next week'), this MUST be null."
    )
    due_date_text: Optional[str] = Field(
        default=None,
        description="The raw text for the due date (e.g., 'next Friday', '3 din mai')."
    )
    due_date_confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Confidence score for the extracted due date."
    )
    urgency_level: UrgencyLevel = Field(
        default=UrgencyLevel.MEDIUM,
        description="Urgency of the commitment. Must match Enum."
    )
    status: str = Field(
        default="pending",
        description="Current status of the commitment."
    )
    confidence: float = Field(
        default=0.9,
        ge=0.0, 
        le=1.0,
        description="AI confidence score."
    )


class ClientIdentificationStatus(str, Enum):
    IDENTIFIED = "identified"
    MULTIPLE_MATCHES = "multiple_matches"
    NOT_FOUND = "not_found"
    # Gemini system prompt "unknown" aur "ambiguous" return karta tha — ab supported hain
    UNKNOWN = "unknown"
    AMBIGUOUS = "ambiguous"


class ClientIdentificationExtraction(BaseModel):
    """
    Identifies which client the meeting is about.
    """
    model_config = ConfigDict(extra="ignore")

    status: ClientIdentificationStatus = Field(
        ...,
        description="Whether a specific client was clearly identified, multiple possible matches exist, or none were found."
    )
    suggested_client_name: Optional[str] = Field(
        default=None,
        description="The exact name of the client mentioned in the meeting, if any."
    )
    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="AI confidence that it correctly identified the client context."
    )


class MeetingExtraction(BaseModel):
    """
    The master output schema for the LLM processing a meeting transcript.
    This is the ONLY contract the LLM is allowed to return.
    Extra fields from Gemini (e.g. matched_client_id) are silently ignored.
    """
    model_config = ConfigDict(extra="ignore")

    client_identification: ClientIdentificationExtraction = Field(
        ...,
        description="Details about which client the meeting belongs to."
    )
    meeting_summary: str = Field(
        ...,
        min_length=5,
        description="A concise summary of the entire meeting."
    )
    key_discussion_points: list[str] = Field(
        default_factory=list,
        description="Bullet points of the main topics discussed."
    )
    products_owned: list[str] = Field(
        default_factory=list,
        description="Financial products the client owns or is interested in."
    )
    concerns: list[RiskSignal] = Field(
        default_factory=list,
        description="Any risks, complaints, or negative sentiments raised. Must be empty if none."
    )
    commitments: list[CommitmentExtraction] = Field(
        default_factory=list,
        description="Any tasks, action items, or promises made. Must be empty if none."
    )
    action_items: list[str] = Field(
        default_factory=list,
        description="Simple string list of action items."
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Any warnings or flags from the AI."
    )
