import json
from urllib.parse import urlencode

import pytest
from aiohttp import ClientSession
from http import HTTPStatus

from .conftest import TEST_FILM_UUID


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"query": "star"}, {"status": HTTPStatus.OK, "length": 8}),
        ({"query": "Mashed"}, {"status": HTTPStatus.NOT_FOUND, "length": 1}),
    ],
)
@pytest.mark.asyncio
async def test_search_films_by_title(
    setup_es_indexes, api_base_url, query_data, expected_answer
):
    async with ClientSession() as session:
        url = f"{api_base_url}/films/search"

        async with session.get(url, params=query_data) as response:
            assert (
                response.status == expected_answer["status"]
            ), f"API response status is not {expected_answer['status']}"
            body = await response.json()
            assert (
                len(body) == expected_answer["length"]
            ), "Response body does not contain expected number of items"


@pytest.mark.asyncio
async def test_film_by_id(api_base_url):
    film_id = TEST_FILM_UUID
    async with ClientSession() as session:
        url = f"{api_base_url}/films/{film_id}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            film = await response.json()
            assert (
                film["uuid"] == film_id
            ), "Returned film ID does not match requested ID"


@pytest.mark.asyncio
async def test_all_films(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/films/"
        query_data = {"page_size": 100}

        async with session.get(url, params=query_data) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            genres = await response.json()
            assert len(genres) == 60, "More genres returned than expected"


@pytest.mark.asyncio
async def test_film_invalid_search_parameters(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/films/search"
        invalid_query_data = {"page_number": "invalid", "page_size": -1}

        async with session.get(url, params=invalid_query_data) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), "Expected validation error"


@pytest.mark.asyncio
async def test_film_search_with_empty_query(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/films/search"
        query_data = {"query": ""}

        async with session.get(url, params=query_data) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"


@pytest.mark.asyncio
async def test_film_search_with_large_page_size(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/search"
        query_data = {"page_size": 10000}

        async with session.get(url, params=query_data) as response:
            assert (
                response.status == HTTPStatus.NOT_FOUND
            ), "Expected validation error for too large page_size"


@pytest.mark.asyncio
async def test_film_search_with_specific_record_count(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/films/search"
        query_data = {"page_size": 5}

        async with session.get(url, params=query_data) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert len(body) == 5, "Number of records returned is not as expected"


@pytest.mark.asyncio
async def test_film_with_negative_page_number(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/films"
        query_data = {"page_number": -1}

        async with session.get(url, params=query_data) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), "Expected validation error for negative page_number"


@pytest.mark.asyncio
async def test_film_with_special_character_id(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/films/%"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.NOT_FOUND
            ), "Expected validation error for special character in film ID"


@pytest.mark.asyncio
async def test_film_cache_hit(redis_client, api_base_url):
    url = f"{api_base_url}/films/search"
    query_data = {"query": "star"}
    cache_key = "api_response:/api/v1/films/search?query=star"

    async with ClientSession() as session:
        async with session.get(url, params=query_data) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK} on first request"
            first_request_body = await response.json()

    cached_data_raw = await redis_client.get(cache_key)
    cached_data = [json.loads(item) for item in json.loads(cached_data_raw)]

    async with ClientSession() as session:
        async with session.get(url, params=query_data) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK} on second request"
            second_request_body = await response.json()

    assert (
        first_request_body == cached_data
    ), "First request data does not match cached data in Redis"
    assert (
        second_request_body == cached_data
    ), "Second request data does not match cached data in Redis"


@pytest.mark.asyncio
async def test_film_cache_key_generation(redis_client, api_base_url):
    query_params = {"query": "star", "page": "1"}
    url = f"{api_base_url}/films/search"

    async with ClientSession() as session:
        async with session.get(url, params=query_params) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"

    query_string = urlencode(sorted(query_params.items()))
    expected_cache_key = f"api_response:/api/v1/films/search?{query_string}"

    assert await redis_client.exists(
        expected_cache_key
    ), "Cache key is not correctly formed or does not exist"
