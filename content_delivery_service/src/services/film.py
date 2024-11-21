from functools import lru_cache
from typing import Any

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends, Request
from redis.asyncio import Redis

from core.config import MOVIES_INDEX
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film as FilmModel
from queries.base import BaseFilter
from queries.film import FilmFilter
from services.base import BaseService


class FilmService(BaseService):
    """
    Service class for interacting with Elasticsearch and Redis to retrieve and cache film data.

    Parameters:
    - request (Request): The request object.
    - redis (Redis): An instance of the Redis client for caching purposes.
    - elastic (AsyncElasticsearch): An instance of the AsyncElasticsearch client for interacting with Elasticsearch.
    - model_class (Type[FilmModel]): The Pydantic BaseModel subclass representing the film data model.
    - index (str): The Elasticsearch index for film data.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def _make_query(self, film_filter: FilmFilter) -> dict:
        """
        Construct the extended Elasticsearch query body based on the provided film filter with pagination.

        Parameters:
        - film_filter (FilmFilter): An instance of FilmFilter containing filtering parameters.

        Returns:
        - The Elasticsearch query body.
        """
        query_body = await super()._make_query(film_filter)
        if film_filter.sort:
            query_body["sort"] = [film_filter.sort]
        if film_filter.genre:
            query_body["query"]["bool"]["must"].append(
                {
                    "nested": {
                        "path": "genres",
                        "query": {"match": {"genres.uuid": film_filter.genre}},
                    }
                }
            )
        try:
            query_body = await super()._enrich_query_with_search(
                film_filter, query_body, "title"
            )
        except AttributeError:
            pass
        return query_body

    async def _make_person_films_query(
        self, base_filter: BaseFilter, person_id: str
    ) -> dict[str, Any]:
        """
        Generates an ES query for retrieving films associated with a person based on the specified base filter.

        Parameters:
        - base_filter (BaseFilter): An instance of the BaseFilter class containing filter criteria.
        - person_id (str): The unique identifier of the person.

        Returns:
        - dict[str, Any]: The Elasticsearch query body.
        """
        query_body = await super()._make_query(base_filter)
        query_body["query"]["bool"]["should"] = [
            {"nested": {"path": role, "query": {"match": {f"{role}.uuid": person_id}}}}
            for role in ["actors", "writers", "directors"]
        ]
        return query_body

    async def get_person_films(
        self, base_filter: BaseFilter, person_id: str
    ) -> list[FilmModel]:
        """
        Retrieves a list of film models associated with a person using the generated Elasticsearch query.

        Parameters:
        - base_filter (BaseFilter): An instance of the BaseFilter class containing filter criteria.
        - person_id (str): The unique identifier of the person.

        Returns:
        - list[FilmModel]: A list of film models associated with the person.
        """
        query_body = await self._make_person_films_query(base_filter, person_id)
        try:
            doc = await self.elasticsearch.search(index=self.index, body=query_body)
        except NotFoundError:
            return []
        return [FilmModel(**film["_source"]) for film in doc["hits"]["hits"]]


@lru_cache()
def get_film_service(
    request: Request,
    redis: Redis = Depends(get_redis),
    elasticsearch: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    """
    Dependency function to get an instance of the FilmService.

    Parameters:
    - request (Request): The request object.
    - redis (Redis): An instance of the Redis client for caching purposes.
    - elasticsearch (AsyncElasticsearch): An instance of the client for interacting with Elasticsearch.

    Returns:
    - FilmService: An instance of the FilmService class.
    """
    return FilmService(
        request=request,
        redis=redis,
        elasticsearch=elasticsearch,
        model_class=FilmModel,
        index=MOVIES_INDEX,
    )
