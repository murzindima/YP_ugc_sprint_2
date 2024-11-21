from datetime import datetime
from uuid import UUID

from schemas.base import UserIDMixin


class Comment(UserIDMixin):
    """User's comment for a movie."""

    movie_id: UUID
    created_at: datetime
    content: str
