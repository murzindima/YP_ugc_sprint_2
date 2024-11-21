from models.base import UUIDMixIn


class Person(UUIDMixIn):
    """
    Pydantic model representing a person.

    Attributes:
    - uuid (uuid.UUID): The universally unique identifier of the person.
    - name (str): The name of the person.
    """

    name: str


class FilmRoles(UUIDMixIn):
    """
    Pydantic model representing a film and its participants.

    Attributes:
    - uuid (uuid.UUID): The universally unique identifier of the film.
    - roles (List[str]): A list of roles associated with the film.
    """

    roles: list[str]


class PersonFilms(UUIDMixIn):
    """
    Pydantic model representing a person and his films.

    This model extends the IdMixIn, inheriting its UUID functionality. It includes:
    - full_name (str): The full name of the person.
    - films (Optional[List[Film]]): An optional list of films associated with the person.

    Attributes:
    - uuid (uuid.UUID): Inherited from IdMixIn, the UUID of the person.
    - full_name (str): The full name of the person.
    - films (Optional[List[Film]]): A list of Film model instances.
    """

    full_name: str
    films: list[FilmRoles] | None = []
