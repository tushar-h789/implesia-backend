import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.order import OrderStatus
from app.schemas.service import ServiceSummary


class OrderCreate(BaseModel):
    service_id: uuid.UUID
    full_name: str = Field(min_length=2, max_length=160)
    email: EmailStr
    phone: str | None = Field(None, max_length=40)
    organisation: str | None = Field(None, max_length=200)
    message: str = Field(min_length=20, max_length=5000)
    source_page: str | None = Field(None, max_length=255)
    turnstile_token: str | None = None
    website: str | None = Field(None, exclude=True)

    @field_validator("full_name", "message")
    @classmethod
    def _strip(cls, value: str) -> str:
        return value.strip()


class OrderUpdate(BaseModel):
    status: OrderStatus | None = None
    internal_notes: str | None = Field(None, max_length=5000)


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    service_id: uuid.UUID
    service: ServiceSummary
    full_name: str
    email: EmailStr
    phone: str | None
    organisation: str | None
    message: str
    status: OrderStatus
    internal_notes: str | None
    source_page: str | None
    created_at: datetime


class OrderSubmissionResponse(BaseModel):
    id: uuid.UUID
    message: str = "Thank you. We received your order and will respond within one business day."
