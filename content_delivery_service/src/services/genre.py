from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from core.config import GENRES_INDEX
from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends, Request
from models.genre import Genre as GenreModel
from services.base import BaseService


class GenreService(BaseService):
    """
    Service class for managing genres, extending the BaseService.

    Parameters:
    - redis (Redis): An instance of the Redis client for caching purposes.
    - elastic (AsyncElasticsearch): An instance of the AsyncElasticsearch client for interacting with Elasticsearch.
    - model_class (Type[GenreModel]): The Pydantic BaseModel subclass representing the Genre data model.
    - index (str): The Elasticsearch index to operate on (specific to genres).
    """


@lru_cache()
def get_genre_service(
    request: Request,
    redis: Redis = Depends(get_redis),
    elasticsearch: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    """
    Factory function to obtain a GenreService instance.

    Parameters:
    - request (Request): The request object.
    - redis (Redis): An instance of the Redis client for caching purposes.
    - elastic (AsyncElasticsearch): An instance of the AsyncElasticsearch client for interacting with Elasticsearch.

    Returns:
    - GenreService: An instance of the GenreService class.
    """
    return GenreService(
        request=request,
        redis=redis,
        elasticsearch=elasticsearch,
        model_class=GenreModel,
        index=GENRES_INDEX,
    )
