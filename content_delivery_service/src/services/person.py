from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends, Request
from redis.asyncio import Redis

from core.config import PERSONS_INDEX
from db.elastic import get_elastic
from db.redis import get_redis
from models.person import PersonFilms as PersonFilmsModel
from queries.person import PersonFilter
from services.base import BaseService


class PersonService(BaseService):
    """
    Service class for interacting with Elasticsearch and Redis to retrieve and cache person data.

    Parameters:
    - redis (Redis): An instance of the Redis client for caching purposes.
    - elastic (AsyncElasticsearch): An instance of the AsyncElasticsearch client for interacting with Elasticsearch.
    - model_class (Type[PersonModel]): The Pydantic BaseModel subclass representing the person data model.
    - index (str): The Elasticsearch index for person data.
    """

    async def _make_query(self, person_filter: PersonFilter) -> dict:
        """
        Construct the Elasticsearch query body based on the provided person filter with pagination.

        Parameters:
        - person_filter (PersonFilter): An instance of PersonFilter containing filtering parameters.

        Returns:
        - The Elasticsearch query body.
        """
        query_body = await super()._make_query(person_filter)
        try:
            query_body = await super()._enrich_query_with_search(
                person_filter, query_body, "full_name"
            )
        except AttributeError:
            pass
        return query_body


@lru_cache()
def get_person_service(
    request: Request,
    redis: Redis = Depends(get_redis),
    elasticsearch: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    """
    Dependency function to get an instance of the PersonService.

    Parameters:
    - request (Request): The request object.
    - redis (Redis): An instance of the Redis client for caching purposes.
    - elastic (AsyncElasticsearch): An instance of the AsyncElasticsearch client for interacting with Elasticsearch.

    Returns:
    - PersonService: An instance of the PersonService class.
    """
    return PersonService(
        request=request,
        redis=redis,
        elasticsearch=elasticsearch,
        model_class=PersonFilmsModel,
        index=PERSONS_INDEX,
    )
