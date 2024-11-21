from schemas.base import CreatedAtMixin, UserIDMixin


class Click(UserIDMixin, CreatedAtMixin):
    """User's click on a resource."""

    resource: str
