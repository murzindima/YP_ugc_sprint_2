from abc import ABC, abstractmethod
from typing import Union


class CacheService[M](ABC):
    """
    Abstract base class defining the interface for a caching service.

    This class is designed to be subclassed for implementing specific caching services
    that interact with different types of models.
    """

    @abstractmethod
    async def get_from_cache(self, cache_key: str) -> Union[M, list[M]] | None:
        """Abstract method to retrieve a model or a list of models from the cache based on the cache key."""

    @abstractmethod
    async def put_to_cache(self, cache_key: str, model: M | list[M]):
        """Abstract method to store a model or a list of models in the cache."""
