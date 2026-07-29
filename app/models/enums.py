from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    MEMBER = "MEMBER"

class MeetingStatus(str, Enum):
    PROCESSING = "processing"
    PROCESSED = "processed"
    MANUAL_REVIEW_REQUIRED = "manual_review_required"
    CLIENT_IDENTIFICATION_REQUIRED = "client_identification_required"
    FAILED = "failed"

class MeetingSourceType(str, Enum):
    PASTED_NOTE = "pasted_note"
    AUDIO_UPLOAD = "audio_upload"
    LIVE_BROWSER = "live_browser"

class CommitmentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
