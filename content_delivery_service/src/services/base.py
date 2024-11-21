from typing import Type

from elasticsearch import AsyncElasticsearch
from fastapi import Request
from pydantic import BaseModel
from redis.asyncio import Redis

from queries.base import BaseFilter
from services.elasticsearch import ElasticsearchService
from services.redis_cache import RedisCacheService


class BaseService[M: BaseModel](RedisCacheService, ElasticsearchService):
    """
    Base service class for interacting with Elasticsearch and Redis for data retrieval and caching.

    Parameters:
    - request (Request): The request object.
    - elasticsearch (AsyncElasticsearch): An instance of client for interacting with Elasticsearch.
    - redis (Redis): An instance of the Redis client for caching purposes.
    - model_class (Type[M]): The Pydantic BaseModel subclass representing the data model for this service.
    - index (str): The Elasticsearch index to operate on.
    """

    def __init__(
        self,
        request: Request,
        elasticsearch: AsyncElasticsearch,
        redis: Redis,
        model_class: Type[M],
        index: str,
    ):
        self.request = request
        ElasticsearchService.__init__(
            self,
            elasticsearch=elasticsearch,
            index=index,
            model_class=model_class,
        )
        RedisCacheService.__init__(
            self,
            redis=redis,
            model_class=model_class,
        )

    async def get_model_by_id(self, model_id: str) -> M | None:
        """
        Retrieve a model by its unique identifier.

        Parameters:
        - model_id (str): The unique identifier of the model.

        Returns:
        - An instance of the model if found, otherwise None.
        """
        cache_key = super().generate_cache_key(self.request)
        model = await super().get_from_cache(cache_key)

        if not model:
            model = await super().get_by_id(model_id)
            if not model:
                return None
            await super().put_to_cache(cache_key, model)

        return model

    async def get_all_models(self, model_filter: BaseFilter) -> list[M]:
        """
        Retrieve multiple models based on the provided filter.

        Parameters:
        - model_filter (BaseFilter): An instance of BaseFilter containing filtering parameters.

        Returns:
        - A list of model instances that match the filter criteria.
        """
        cache_key = super().generate_cache_key(self.request)
        models = await super().get_from_cache(cache_key)

        if not models:
            models = await super().get_all(model_filter)
            if not models:
                return []
            await super().put_to_cache(cache_key, models)

        return models
