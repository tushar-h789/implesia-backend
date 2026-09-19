import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.lead import LeadStatus, ServiceArea, Timeline


class LeadCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=160)
    email: EmailStr
    phone: str | None = Field(None, max_length=40)
    organisation: str | None = Field(None, max_length=200)
    service_area: ServiceArea | None = None
    timeline: Timeline | None = None
    brief: str = Field(min_length=20, max_length=5000)
    source_page: str | None = Field(None, max_length=255)
    turnstile_token: str | None = None

    # Hidden field that real users never fill in; bots usually do.
    website: str | None = Field(None, exclude=True)

    @field_validator("full_name", "brief")
    @classmethod
    def _strip(cls, value: str) -> str:
        return value.strip()


class LeadUpdate(BaseModel):
    status: LeadStatus | None = None
    internal_notes: str | None = Field(None, max_length=5000)


class LeadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str
    email: EmailStr
    phone: str | None
    organisation: str | None
    service_area: ServiceArea | None
    timeline: Timeline | None
    brief: str
    status: LeadStatus
    internal_notes: str | None
    source_page: str | None
    created_at: datetime


class LeadSubmissionResponse(BaseModel):
    id: uuid.UUID
    message: str = "Thank you. We will respond within one business day."
