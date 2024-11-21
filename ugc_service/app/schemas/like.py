from uuid import UUID

from schemas.base import CreatedAtMixin, UserIDMixin


class Like(UserIDMixin, CreatedAtMixin):
    """User's like for a movie."""

    movie_id: UUID
