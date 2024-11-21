from schemas.base import UUIDMixIn


class Genre(UUIDMixIn):
    """
    Pydantic model representing a film genre API schema.

    Attributes:
    - uuid (uuid.UUID): The universally unique identifier of the genre.
    - name (str): The name of the genre.
    """

    name: str
