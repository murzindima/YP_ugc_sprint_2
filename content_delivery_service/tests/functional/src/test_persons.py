import json
from http import HTTPStatus
from urllib.parse import urlencode

import pytest
from aiohttp import ClientSession

from .conftest import TEST_PERSON_UUIDS


@pytest.mark.asyncio
async def test_all_persons_pagination(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/persons/"
        query_data = {"page_size": 5}

        async with session.get(url, params=query_data) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            persons = await response.json()
            assert len(persons) <= 5, "More persons returned than expected"


@pytest.mark.asyncio
async def test_all_persons(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/persons/"
        query_data = {"page_size": 100}

        async with session.get(url, params=query_data) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            persons = await response.json()
            assert len(persons) == 4, "More persons returned than expected"


@pytest.mark.asyncio
async def test_search_persons_by_name(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/persons/search"
        query_data = {"query": "John"}

        async with session.get(url, params=query_data) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            persons = await response.json()
            assert all(
                "John" in person["full_name"] for person in persons
            ), "Search results do not match query"


@pytest.mark.asyncio
async def test_person_details_by_id(api_base_url):
    person_id = TEST_PERSON_UUIDS["John Doe"]
    async with ClientSession() as session:
        url = f"{api_base_url}/persons/{person_id}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            person = await response.json()
            assert (
                person["uuid"] == person_id
            ), "Returned person ID does not match requested ID"


@pytest.mark.asyncio
async def test_person_films(api_base_url):
    person_id = TEST_PERSON_UUIDS["John Doe"]
    async with ClientSession() as session:
        url = f"{api_base_url}/persons/{person_id}/film"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            films = await response.json()
            assert len(films) == 10, "More persons returned than expected"


@pytest.mark.asyncio
async def test_person_cache_hit(redis_client, api_base_url):
    url = f"{api_base_url}/persons/search"
    query_data = {"query": "John"}
    cache_key = "api_response:/api/v1/persons/search?query=John"

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
async def test_person_cache_key_generation(redis_client, api_base_url):
    query_params = {"query": "John", "page": "1"}
    url = f"{api_base_url}/persons/search"

    async with ClientSession() as session:
        async with session.get(url, params=query_params) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"

    query_string = urlencode(sorted(query_params.items()))
    expected_cache_key = f"api_response:/api/v1/persons/search?{query_string}"

    assert await redis_client.exists(
        expected_cache_key
    ), "Cache key is not correctly formed or does not exist"
