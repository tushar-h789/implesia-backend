import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=160)
    role: UserRole = UserRole.VIEWER
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(min_length=12, max_length=72)


class UserUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=1, max_length=160)
    role: UserRole | None = None
    is_active: bool | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    last_login_at: datetime | None
    created_at: datetime
