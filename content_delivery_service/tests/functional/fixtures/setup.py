import pytest
import pytest_asyncio
from elasticsearch.helpers import async_bulk

from functional.testdata.es_mapping import (
    FILMS_INDEX_MAPPING,
    GENRES_INDEX_MAPPING,
    PERSONS_INDEX_MAPPING,
)


@pytest_asyncio.fixture()
async def setup_es_indexes(es_client, es_data_films, es_data_genres, es_data_persons):
    es_indexes = {
        "films": {
            "index": "movies",
            "mapping": FILMS_INDEX_MAPPING,
            "data": es_data_films,
        },
        "genres": {
            "index": "genres",
            "mapping": GENRES_INDEX_MAPPING,
            "data": es_data_genres,
        },
        "persons": {
            "index": "persons",
            "mapping": PERSONS_INDEX_MAPPING,
            "data": es_data_persons,
        },
    }

    for index in es_indexes.values():
        es_index = index["index"]
        es_index_mapping = index["mapping"]
        bulk_query = [
            {"_index": es_index, "_id": data["uuid"], "_source": data}
            for data in index["data"]
        ]
        if await es_client.indices.exists(index=es_index):
            await es_client.indices.delete(index=es_index)
        await es_client.indices.create(index=es_index, **es_index_mapping)
        inserted_documents, errors = await async_bulk(
            client=es_client, actions=bulk_query, refresh="wait_for"
        )
        if errors:
            pytest.fail(f"Errors while loading data to ES: {errors}")
        assert inserted_documents == len(
            index["data"]
        ), f"Not all documents for {es_index} were inserted successfully."
