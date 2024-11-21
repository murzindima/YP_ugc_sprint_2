import pytest
from aiohttp import ClientSession
from http import HTTPStatus

from tests.functional.fixtures.common import USER_ID, MOVIE_ID

pytestmark = pytest.mark.asyncio
LIKE_ID_TO_UPDATE: str | None = None
LIKE_ID_TO_DELETE: str | None = None


async def test_get_likes_wo_auth(ugc_api_likes_url):
    async with ClientSession() as session:
        url = f"{ugc_api_likes_url}/{MOVIE_ID}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


async def test_get_likes(ugc_api_likes_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_likes_url}/{MOVIE_ID}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert isinstance(body, list)
            assert len(body) >= 0
            assert all([x["movie_id"] == MOVIE_ID for x in body])
            assert all([x["user_id"] == USER_ID for x in body])
            assert all(["_id" in x for x in body])
            assert all(["score" in x for x in body])


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (
            {
                "user_id": USER_ID,
                "movie_id": MOVIE_ID,
                "score": 0,
            },
            {"status": HTTPStatus.CREATED},
        ),
        (
            {
                "user_id": USER_ID,
                "movie_id": MOVIE_ID,
                "score": 0,
            },
            {"status": HTTPStatus.CREATED},
        ),
        (
            {
                "user_id": USER_ID,
                "movie_id": "3fa85f64-5717-4562-b3fc-2c963f64afa9",
                "score": 5,
            },
            {"status": HTTPStatus.CREATED},
        ),
        (
            {
                "user_id": USER_ID,
                "movie_id": "3fa85f64-5717-4562-b3fc-2c963f64af10",
                "score": 10,
            },
            {"status": HTTPStatus.CREATED},
        ),
    ],
)
async def test_create_like_ok(ugc_api_likes_url, access_token, test_data, expected):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_likes_url}/"

        async with session.post(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"
            body = await response.json()
            assert "_id" in body
            assert body["movie_id"] == test_data["movie_id"]
            assert body["user_id"] == test_data["user_id"]
            assert body["score"] == test_data["score"]


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (
            {
                "user_id": "3fa85f64-5717-4562-b3fc-2c333f64afa6",
                "movie_id": MOVIE_ID,
                "score": 4,
            },
            {"status": HTTPStatus.CREATED},
        ),
    ],
)
async def test_create_like_to_update(
    ugc_api_likes_url, access_token, test_data, expected
):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_likes_url}/"

        async with session.post(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"
            body = await response.json()
            assert "_id" in body
            assert body["movie_id"] == test_data["movie_id"]
            assert body["user_id"] == test_data["user_id"]
            assert body["score"] == test_data["score"]
            global LIKE_ID_TO_UPDATE
            LIKE_ID_TO_UPDATE = body["_id"]


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (
            {
                "user_id": "3fa85f64-5717-4562-b322-2c333f64afa6",
                "movie_id": MOVIE_ID,
                "score": 7,
            },
            {"status": HTTPStatus.CREATED},
        ),
    ],
)
async def test_create_like_to_delete(
    ugc_api_likes_url, access_token, test_data, expected
):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_likes_url}/"

        async with session.post(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"
            body = await response.json()
            assert "_id" in body
            assert body["movie_id"] == test_data["movie_id"]
            assert body["user_id"] == test_data["user_id"]
            assert body["score"] == test_data["score"]
            global LIKE_ID_TO_DELETE
            LIKE_ID_TO_DELETE = body["_id"]


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (
            {
                "user_id": USER_ID,
                "movie_id": MOVIE_ID,
                "score": "5",
            },
            {"status": HTTPStatus.UNAUTHORIZED},
        ),
    ],
)
async def test_create_like_wo_auth(ugc_api_likes_url, test_data, expected):
    async with ClientSession() as session:
        url = f"{ugc_api_likes_url}/"

        async with session.post(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (
            {
                "user_id": USER_ID,
                "movie_id": MOVIE_ID,
                "score": -1,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "user_id": USER_ID,
                "movie_id": MOVIE_ID,
                "score": 11,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "user_id": USER_ID,
                "movie_id": MOVIE_ID,
                "score": 100,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "user_id": USER_ID,
                "movie_id": MOVIE_ID,
                "score": -5,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "user_id": USER_ID,
                "movieid": MOVIE_ID,
                "score": 5,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "userid": USER_ID,
                "movie_id": MOVIE_ID,
                "score": 5,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "user_id": USER_ID,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "movie_id": MOVIE_ID,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "score": 4,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "sdf": MOVIE_ID,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
    ],
)
async def test_create_like_notok(ugc_api_likes_url, access_token, test_data, expected):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_likes_url}/"

        async with session.post(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"


async def test_update_like_wo_auth(ugc_api_likes_url):
    async with ClientSession() as session:
        url = f"{ugc_api_likes_url}/{LIKE_ID_TO_UPDATE}"

        async with session.put(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (
            {
                "user_id": USER_ID,
                "movie_id": MOVIE_ID,
                "score": 3,
            },
            {"status": HTTPStatus.OK},
        ),
        (
            {
                "user_id": "3fa85f64-5717-4533-b3fc-2c963f66afa6",
                "movie_id": MOVIE_ID,
                "score": 2,
            },
            {"status": HTTPStatus.OK},
        ),
        (
            {
                "user_id": USER_ID,
                "movie_id": "3fa85f64-5717-4562-b3fc-2c963f64afa6",
                "score": 4,
            },
            {"status": HTTPStatus.OK},
        ),
        (
            {
                "user_id": USER_ID,
                "movie_id": MOVIE_ID,
                "score": 10,
            },
            {"status": HTTPStatus.OK},
        ),
    ],
)
async def test_update_like_ok(ugc_api_likes_url, access_token, test_data, expected):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_likes_url}/{LIKE_ID_TO_UPDATE}"

        async with session.put(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"
            body = await response.json()
            assert "_id" in body
            assert body["movie_id"] == test_data["movie_id"]
            assert body["user_id"] == test_data["user_id"]
            assert body["score"] == test_data["score"]


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (
            {
                "user_id": USER_ID,
                "movie_id": MOVIE_ID,
                "score": -1,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "user_id": USER_ID,
                "movie_id": MOVIE_ID,
                "score": 11,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "user_id": USER_ID,
                "movie_id": MOVIE_ID,
                "score": 100,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "user_id": USER_ID,
                "movie_id": MOVIE_ID,
                "score": -5,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "user_id": USER_ID,
                "movieid": MOVIE_ID,
                "score": 5,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "userid": USER_ID,
                "movie_id": MOVIE_ID,
                "score": 5,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "user_id": USER_ID,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "movie_id": MOVIE_ID,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "score": 4,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "sdf": MOVIE_ID,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
    ],
)
async def test_update_like_notok(ugc_api_likes_url, access_token, test_data, expected):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_likes_url}/{LIKE_ID_TO_UPDATE}"

        async with session.put(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"


async def test_delete_like_wo_auth(ugc_api_likes_url):
    async with ClientSession() as session:
        url = f"{ugc_api_likes_url}/{LIKE_ID_TO_DELETE}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


async def test_delete_like_ok_existed(ugc_api_likes_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_likes_url}/{LIKE_ID_TO_DELETE}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert body["deleted_count"] == 1
            assert body["_id"] == LIKE_ID_TO_DELETE


async def test_delete_like_ok_notexisted(ugc_api_likes_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_likes_url}/{LIKE_ID_TO_DELETE}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert body["deleted_count"] == 0
            assert body["_id"] == LIKE_ID_TO_DELETE


async def test_delete_like_not_ok(ugc_api_likes_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_likes_url}/qwe"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"
