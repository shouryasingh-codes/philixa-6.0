from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class RegisterRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=8, max_length=72)
    workspace_name: str = Field(..., min_length=1, max_length=120)
    workspace_type: str = Field(default="company", max_length=20)


class LoginRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=1, max_length=72)


class VerifyEmailRequest(BaseModel):
    token: str = Field(..., min_length=1)


class ForgotPasswordRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=72)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    is_verified: bool
    is_active: bool
    created_at: Optional[datetime] = None


class OrganizationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    slug: str
    workspace_type: str
    plan: str
    is_active: bool = True
    created_at: Optional[datetime] = None


class MembershipRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    organization_id: str
    organization_name: str
    slug: Optional[str] = None
    organization_slug: Optional[str] = None
    workspace_type: Optional[str] = None
    role: str
    status: str
    joined_at: Optional[datetime] = None


class LoginResponse(BaseModel):
    user: UserRead
    active_organization: OrganizationRead
    role: str
    csrf_token: Optional[str] = None


class RegisterResponse(BaseModel):
    message: str
    user: Optional[UserRead] = None
    organization: Optional[OrganizationRead] = None


class UserProfileResponse(BaseModel):
    user: UserRead
    active_organization: OrganizationRead
    role: str
    session_id: Optional[str] = None
    memberships: list[MembershipRead] = Field(default_factory=list)


class TokenRefreshResponse(BaseModel):
    message: str
    csrf_token: Optional[str] = None


class MessageResponse(BaseModel):
    message: str
    verified: Optional[bool] = None
    detail: Optional[str] = None
