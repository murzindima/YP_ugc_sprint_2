from pydantic import BaseModel


class UUIDMixIn(BaseModel):
    """Mixin class providing a universally unique identifier (UUID) attribute."""

    uuid: str
