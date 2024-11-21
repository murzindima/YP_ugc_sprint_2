from typing import Annotated

from fastapi import Query

from queries.base import BaseFilter


class PersonFilter(BaseFilter):
    """Represents a filter based on person criteria."""


class SearchPersonFilter(PersonFilter):
    """
    Represents a filter for searching persons based on query criteria.

    Attributes:
        query (Annotated[str | None, Query()]): The search query for persons.
    """

    query: Annotated[str | None, Query()] = None
