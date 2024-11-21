import json
from typing import Any

from schemas.base import UserIDMixin


class MovieFilterRequest(UserIDMixin):
    """User's search filter request."""

    filters: dict[str, Any]

    @classmethod
    def from_json(cls, filters: str):
        parsed_data = json.loads(filters)
        return cls(filters=parsed_data)
