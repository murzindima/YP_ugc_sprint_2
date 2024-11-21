from uuid import UUID

from schemas.base import CreatedAtMixin, UserIDMixin


class MovieWatchTime(UserIDMixin, CreatedAtMixin):
    """The progress of the user viewing the movie."""

    movie_id: UUID
    seconds_amt: int
    total_seconds_amt: int
