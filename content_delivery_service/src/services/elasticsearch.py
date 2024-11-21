from typing import Any, Type

from elasticsearch import AsyncElasticsearch, NotFoundError
from pydantic import BaseModel

from queries.base import BaseFilter
from services.abstract.data_storage import DataStorageService


class ElasticsearchService[M: BaseModel](DataStorageService):
    """
    A data storage service implementation for working with Elasticsearch.

    This class extends the abstract DataStorageService and provides methods for interacting with
    Elasticsearch to retrieve models by their unique identifier or based on specific filtering criteria.

    Attributes:
        - elasticsearch (AsyncElasticsearch): An instance of the AsyncElasticsearch client.
        - index (str): The Elasticsearch index where the data is stored.
        - model_class (Type[M]): The Pydantic model type associated with the data stored in Elasticsearch.
    """

    def __init__(
        self,
        elasticsearch: AsyncElasticsearch,
        index: str,
        model_class: Type[M],
    ):
        self.elasticsearch = elasticsearch
        self.index = index
        self.model_class = model_class

    async def get_by_id(self, model_id: str) -> M | None:
        """
        Retrieve a model from Elasticsearch by its unique identifier.

        Parameters:
        - model_id (str): The unique identifier of the model.

        Returns:
        - An instance of the model if found, otherwise None.
        """
        try:
            doc = await self.elasticsearch.get(index=self.index, id=model_id)
        except NotFoundError:
            return None
        return self.model_class(**doc["_source"])

    async def get_all(self, model_filter: BaseFilter) -> list[M]:
        """
        Retrieve multiple models from Elasticsearch based on the provided filter.

        Parameters:
        - model_filter (BaseFilter): An instance of BaseFilter containing filtering parameters.

        Returns:
        - A list of model instances that match the filter criteria.
        """
        query_body = await self._make_query(model_filter)
        try:
            doc = await self.elasticsearch.search(index=self.index, body=query_body)
        except NotFoundError:
            return []
        return [self.model_class(**model["_source"]) for model in doc["hits"]["hits"]]

    @staticmethod
    async def _make_query(model_filter: BaseFilter) -> dict[str, Any]:
        """
        Construct the Elasticsearch query body based on the provided filter with pagination.

        Parameters:
        - model_filter (BaseFilter): An instance of BaseFilter containing filtering parameters.

        Returns:
        - The Elasticsearch query body.
        """
        query_body = {
            "query": {
                "bool": {
                    "must": [],
                },
            },
            "size": model_filter.page_size,
            "from": (model_filter.page_number - 1) * model_filter.page_size,
        }
        return query_body

    @staticmethod
    async def _enrich_query_with_search(
        model_filter: BaseFilter, query_body: dict[str, Any], field: str
    ) -> dict[str, Any]:
        """
        Enrich the Elasticsearch query with a fuzzy search.

        Parameters:
        - model_filter (BaseFilter): An instance of BaseFilter containing search parameters.
        - query_body (dict[str, Any]): The Elasticsearch query body.
        - field (str): The field to perform the fuzzy search on.

        Returns:
        - The modified Elasticsearch query body.
        """
        if model_filter.query:
            query_body["query"]["bool"]["must"].append(
                {
                    "fuzzy": {
                        field: {"value": model_filter.query, "fuzziness": "AUTO"},
                    },
                },
            )
        return query_body
