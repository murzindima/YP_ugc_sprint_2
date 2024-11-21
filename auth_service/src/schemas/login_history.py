from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class LoginHistory(BaseModel):
    """Schema for a user login history."""

    id: UUID
    user_id: UUID
    timestamp: datetime | None
    ip_address: str | None
    location: str | None
    os: str | None
    browser: str | None
    device: str | None
    refresh_token: str
    is_active: bool | None = True

    class Config:
        from_attributes = True
