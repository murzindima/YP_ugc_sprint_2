import pytest
from aiohttp import ClientSession
from http import HTTPStatus

from tests.functional.fixtures.common import USER_ID, MOVIE_ID

pytestmark = pytest.mark.asyncio
BOOKMARK_ID_TO_DELETE: str | None = None


async def test_get_bookmarks_wo_auth(ugc_api_bookmarks_url):
    async with ClientSession() as session:
        url = f"{ugc_api_bookmarks_url}/{USER_ID}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


async def test_get_bookmarks(ugc_api_bookmarks_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_bookmarks_url}/{USER_ID}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert isinstance(body, list)
            assert len(body) >= 0
            assert all([bookmark["user_id"] == USER_ID for bookmark in body])
            assert all([bookmark["movie_id"] == MOVIE_ID for bookmark in body])
            assert all([bookmark["_id"] for bookmark in body])


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (
            {
                "user_id": USER_ID,
                "movie_id": MOVIE_ID,
            },
            {"status": HTTPStatus.CREATED},
        ),
    ],
)
async def test_create_bookmark_ok(
    ugc_api_bookmarks_url, access_token, test_data, expected
):

    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_bookmarks_url}/"

        async with session.post(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"
            body = await response.json()
            assert "_id" in body
            assert body["movie_id"] == test_data["movie_id"]
            assert body["user_id"] == test_data["user_id"]
            global BOOKMARK_ID_TO_DELETE
            BOOKMARK_ID_TO_DELETE = body["_id"]


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (
            {
                "user_id": USER_ID,
                "movie_id": MOVIE_ID,
            },
            {"status": HTTPStatus.UNAUTHORIZED},
        ),
    ],
)
async def test_create_bookmark_wo_auth(ugc_api_bookmarks_url, test_data, expected):
    async with ClientSession() as session:
        url = f"{ugc_api_bookmarks_url}/"

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
                "movieid": MOVIE_ID,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "userid": USER_ID,
                "movie_id": MOVIE_ID,
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
async def test_create_bookmark_notok(
    ugc_api_bookmarks_url, access_token, test_data, expected
):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_bookmarks_url}/"

        async with session.post(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"


async def test_delete_bookmark_wo_auth(ugc_api_bookmarks_url):
    async with ClientSession() as session:
        url = f"{ugc_api_bookmarks_url}/{BOOKMARK_ID_TO_DELETE}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


async def test_delete_bookmark_ok_existed(ugc_api_bookmarks_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_bookmarks_url}/{BOOKMARK_ID_TO_DELETE}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert body["deleted_count"] == 1
            assert body["_id"] == BOOKMARK_ID_TO_DELETE


async def test_delete_bookmark_ok_notexisted(ugc_api_bookmarks_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_bookmarks_url}/{BOOKMARK_ID_TO_DELETE}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert body["deleted_count"] == 0
            assert body["_id"] == BOOKMARK_ID_TO_DELETE


async def test_delete_bookmark_not_ok(ugc_api_bookmarks_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_bookmarks_url}/qwe"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"
