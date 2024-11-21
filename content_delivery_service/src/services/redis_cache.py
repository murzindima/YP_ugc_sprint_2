import json
from typing import Type, Union
from urllib.parse import urlencode

from fastapi import Request
from pydantic import BaseModel
from redis.asyncio import Redis

from services.abstract.cache import CacheService

CACHE_EXPIRE_IN_SECONDS = 60 * 5
CACHE_NAMESPACE = "api_response"


class RedisCacheService[M: BaseModel](CacheService):
    """
    A caching service implementation for working with Redis.

    This class extends the abstract CacheService and provides methods for retrieving models
    or lists of models from the Redis cache and storing them in the cache.

    Attributes:
        - redis (Redis): An instance of the Redis client.
        - model_class (Type[M]): The Pydantic model type associated with the data to be cached.
    """

    def __init__(self, redis: Redis, model_class: Type[M]):
        self.redis = redis
        self.model_class = model_class

    async def get_from_cache(self, cache_key: str) -> Union[M, list[M]] | None:
        """
        Retrieve a model or list of models from the Redis cache.

        Parameters:
        - cache_key (str): The unique key for retrieving the data.

        Returns:
        - An instance of the model or a list of model instances if found in the cache, otherwise None.
        """
        data = await self.redis.get(cache_key)
        if not data:
            return None

        try:
            deserialized_data = json.loads(data)
        except json.JSONDecodeError:
            return None

        if isinstance(deserialized_data, list):
            return [
                self.model_class.model_validate_json(item) for item in deserialized_data
            ]

        return self.model_class.model_validate_json(json.dumps(deserialized_data))

    async def put_to_cache(self, cache_key: str, model: M | list[M]):
        """
        Put a model or list of models into the Redis cache.

        Parameters:
        - model (M | list[M]): An instance of the model or a list of models to be cached.
        """
        if isinstance(model, list):
            serialized_data = json.dumps([m.model_dump_json() for m in model])
        else:
            serialized_data = model.model_dump_json()

        await self.redis.set(cache_key, serialized_data, CACHE_EXPIRE_IN_SECONDS)

    @staticmethod
    def generate_cache_key(request: Request) -> str:
        """
        Generate a unique cache key based on the request's path and query parameters.

        Parameters:
        - request (Request): The FastAPI Request object containing information about the HTTP request.

        Returns:
            - str: A unique cache key derived from the request's path and query parameters.
        """
        namespace = CACHE_NAMESPACE
        path = request.url.path
        sorted_query_params = sorted(request.query_params.items())
        query_string = urlencode(sorted_query_params)

        return f"{namespace}:{path}?{query_string}"
