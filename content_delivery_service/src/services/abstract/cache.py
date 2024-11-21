from abc import ABC, abstractmethod
from typing import Union

from pydantic import BaseModel


class CacheService[M: BaseModel](ABC):
    """
    Abstract base class defining the interface for a caching service.

    This class is designed to be subclassed for implementing specific caching services
    that interact with different types of models using Pydantic for data validation.

    Attributes:
        - M (BaseModel): The Pydantic model type that the caching service works with.
    """

    @abstractmethod
    async def get_from_cache(self, cache_key: str) -> Union[M, list[M]] | None:
        """
        Abstract method to retrieve a model or a list of models from the cache based on the cache key.

        Parameters:
            - cache_key (str): The key used to identify the cached data.

        Returns:
            - Union[M, list[M]] | None: The retrieved model or list of models if found, else None.
        """

    @abstractmethod
    async def put_to_cache(self, cache_key: str, model: M | list[M]):
        """
        Abstract method to store a model or a list of models in the cache.

        Parameters:
            - cache_key (str): The key used to identify the cached data.
            - model (M | list[M]): The model or list of models to be stored in the cache.
        """
