from uuid import UUID

from schemas.base import CreatedAtMixin, UserIDMixin


class Bookmark(UserIDMixin, CreatedAtMixin):
    """User's bookmark for a movie."""

    movie_id: UUID
