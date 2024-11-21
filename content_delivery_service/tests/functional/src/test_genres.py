import json
from http import HTTPStatus

import pytest
from aiohttp import ClientSession

from .conftest import TEST_GENRE_UUIDS


@pytest.mark.asyncio
async def test_all_genres_pagination(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/genres/"
        query_data = {"page_size": 1}

        async with session.get(url, params=query_data) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            genres = await response.json()
            assert len(genres) <= 1, "More genres returned than expected"


@pytest.mark.asyncio
async def test_all_genres(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/genres/"
        query_data = {"page_size": 100}

        async with session.get(url, params=query_data) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            genres = await response.json()
            assert len(genres) == 5, "More genres returned than expected"


@pytest.mark.asyncio
async def test_genre_by_id(api_base_url):
    genre_id = TEST_GENRE_UUIDS["Action"]
    async with ClientSession() as session:
        url = f"{api_base_url}/genres/{genre_id}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            genre = await response.json()
            assert (
                genre["uuid"] == genre_id
            ), "Returned genre ID does not match requested ID"


@pytest.mark.asyncio
async def test_genre_cache_hit(redis_client, api_base_url):
    genre_id = TEST_GENRE_UUIDS["Action"]
    url = f"{api_base_url}/genres/{genre_id}"
    cache_key = f"api_response:/api/v1/genres/{genre_id}?"

    async with ClientSession() as session:
        async with session.get(
            url,
        ) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK} on first request"
            first_request_body = await response.json()

    cached_data_raw = await redis_client.get(cache_key)
    cached_data = json.loads(cached_data_raw)

    async with ClientSession() as session:
        async with session.get(url) as response:
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
async def test_genre_cache_key_generation(redis_client, api_base_url):
    genre_id = TEST_GENRE_UUIDS["Action"]
    url = f"{api_base_url}/genres/{genre_id}"

    async with ClientSession() as session:
        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"

    expected_cache_key = f"api_response:/api/v1/genres/{genre_id}?"

    assert await redis_client.exists(
        expected_cache_key
    ), "Cache key is not correctly formed or does not exist"
