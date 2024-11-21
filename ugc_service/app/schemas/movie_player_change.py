from enum import Enum
from uuid import UUID

from schemas.base import UserIDMixin


class ChangeType(str, Enum):
    LANGUAGE = "language"
    QUALITY = "quality"


class MoviePlayerChange(UserIDMixin):
    """User's movie player change."""

    movie_id: UUID
    change_type: ChangeType
    old_value: str
    new_value: str
