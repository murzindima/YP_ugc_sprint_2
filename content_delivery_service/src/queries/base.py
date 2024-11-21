from typing import Annotated

from fastapi import Query
from pydantic import BaseModel


class BaseFilter(BaseModel):
    """
    Base class for filters with pagination support.

    Attributes:
        page_number (Annotated[int | None, Query(gt=0)]): The page number for paginated results.
        page_size (Annotated[int | None, Query(gt=0)]): The number of items per page in paginated results.
    """

    page_number: Annotated[int | None, Query(gt=0)] = 1
    page_size: Annotated[int | None, Query(gt=0)] = 10
