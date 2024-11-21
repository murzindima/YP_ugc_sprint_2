from enum import Enum
from typing import Annotated

from fastapi import Query
from pydantic import field_validator

from queries.base import BaseFilter


class SortOptions(str, Enum):
    IMDB_RATING = "imdb_rating"
    IMDB_RATING_DESC = "-imdb_rating"


class FilmFilter(BaseFilter):
    """
    Represents a filter for films based on genre and sorting criteria.

    Attributes:
        genre (Annotated[str | None, Query()]): The genre to filter films by.
        sort (Annotated[SortOptions | None, Query()]): The sorting option for films.
    """

    genre: Annotated[str | None, Query()] = None
    sort: Annotated[SortOptions | None, Query()] = None

    @field_validator("sort")
    @classmethod
    def parse_sort(cls, value: str | None) -> dict[str, str] | None:
        """
        Parses the sorting option from the provided value.

        Parameters:
            value (str | None): The sorting option.

        Returns:
            dict[str, str] | None: A dictionary representing the parsed sorting option.
        """
        if value:
            return {
                value.removeprefix("-"): {
                    "order": "desc" if value.startswith("-") else "asc"
                },
            }
        return None


class SearchFilmFilter(FilmFilter):
    """
    Represents a filter for searching films based on query criteria.

    Attributes:
        query (Annotated[str | None, Query()]): The search query for films.
    """

    query: Annotated[str | None, Query()] = None
