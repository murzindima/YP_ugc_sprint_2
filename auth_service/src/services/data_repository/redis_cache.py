import json
from typing import Union

from redis.asyncio import Redis

from src.core.config import app_settings
from src.services.abstract.cache import CacheService


class RedisCacheService(CacheService):
    """A caching service implementation for working with Redis."""

    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_from_cache(self, cache_key: str) -> Union[str, list[str]] | None:
        """Retrieve a model or list of models from the Redis cache."""
        data = await self.redis.get(cache_key)
        if not data:
            return None

        try:
            deserialized_data = json.loads(data)
        except json.JSONDecodeError:
            return None

        return deserialized_data

    async def put_to_cache(self, cache_key: str, model: str | list[str]):
        """Put a model or list of models into the Redis cache."""
        await self.redis.set(cache_key, model, app_settings.access_token_expires)
