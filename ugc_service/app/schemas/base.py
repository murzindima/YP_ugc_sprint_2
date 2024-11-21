from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserIDMixin(BaseModel):
    """Mixin for including user_id information."""

    user_id: UUID | None = None


class CreatedAtMixin(BaseModel):
    """Mixin for including created_at timestamp."""

    created_at: datetime
