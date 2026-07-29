from datetime import date
from pydantic import BaseModel, ConfigDict

class FollowUpTaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    client_id: int
    client_name: str | None = None
    commitment_id: int | None
    description: str
    due_date: date | None
    is_completed: bool
    is_overdue: bool
    is_due_today: bool

class RiskSignalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    client_id: int
    client_name: str | None = None
    meeting_id: int | None
    description: str
    severity_level: str
    confidence: float
    is_high_risk: bool
    requires_review: bool

class DailyPrioritiesResponse(BaseModel):
    tasks: list[FollowUpTaskRead]
    risks: list[RiskSignalRead]
