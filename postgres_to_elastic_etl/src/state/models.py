import uuid
from datetime import datetime

from pydantic import BaseModel


class UUIDMixIn(BaseModel):
    """
    A mixin class for Pydantic models to provide a UUID identifier.

    This mixin class adds a universally unique identifier (UUID) field to
    Pydantic models. It's designed to be used as a base class, providing a
    consistent `id` field for all derived model classes.
    """

    uuid: str | uuid.UUID


class ModifiedMixIn(BaseModel):
    """
    A mixin class for Pydantic models to provide a modified timestamp.

    This mixin class adds a timestamp field to Pydantic models. It's designed
    to be used as a base class, providing a consistent `modified` field for
    all derived model classes.
    """

    modified: datetime


class FilmRoles(UUIDMixIn):
    """
    Pydantic model representing a film.

    Attributes:
    - uuid (uuid.UUID): The universally unique identifier of the film.
    - roles (List[str]): A list of roles associated with the film.
    """

    roles: list[str]


class PersonFilms(UUIDMixIn, ModifiedMixIn):
    """
    Pydantic model representing a person.

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


class Genre(UUIDMixIn, ModifiedMixIn):
    """
    Pydantic model representing a genre.

    This model extends the IdMixIn, inheriting its UUID functionality,
    and includes a `name` field to store the genre's name.
    """

    name: str


class Person(UUIDMixIn):
    """
    Pydantic model representing a person.

    Attributes:
    - uuid (uuid.UUID): Inherited from IdMixIn, the UUID of the person.
    - name (str): The full name of the person.
    """

    name: str


class Movie(UUIDMixIn):
    """
    Pydantic model representing a movie.

    This model includes various fields to represent different attributes of a movie,
    such as title, description, rating, last modification time, genre, director,
    list of actors, and writers. Each actor and writer is represented by a `Person` object.
    Inherits the UUID functionality from IdMixIn.
    """

    title: str
    description: str
    rating: float | None
    modified: datetime
    genres: list[Genre]
    directors: list[Person]
    actors: list[Person]
    writers: list[Person]
