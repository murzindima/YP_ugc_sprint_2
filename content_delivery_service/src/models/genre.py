from models.base import UUIDMixIn


class Genre(UUIDMixIn):
    """
    Pydantic model representing a film genre.

    Attributes:
    - uuid (uuid.UUID): The universally unique identifier of the genre.
    - name (str): The name of the genre.
    """

    name: str
