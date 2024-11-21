import pytest
from aiohttp import ClientSession
from http import HTTPStatus

from tests.functional.fixtures.common import USER_ID, MOVIE_ID

pytestmark = pytest.mark.asyncio
REVIEW_ID_TO_DELETE: str | None = None
REVIEW_ID_TO_LIKE: str | None = None
REVIEW_ID_TO_DISLIKE: str | None = None


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (
            {
                "user_id": USER_ID,
                "movie_id": MOVIE_ID,
                "text": "string",
                "date_published": "2024-03-12T23:55:31.589000",
                "likes": 1,
                "dislikes": 2,
                "movie_score": 10,
            },
            {"status": HTTPStatus.CREATED},
        ),
    ],
)
async def test_create_review_ok(ugc_api_reviews_url, access_token, test_data, expected):

    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_reviews_url}/"

        async with session.post(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"
            body = await response.json()
            assert "_id" in body
            assert body["movie_id"] == test_data["movie_id"]
            assert body["user_id"] == test_data["user_id"]
            assert body["text"] == test_data["text"]
            assert body["date_published"] == test_data["date_published"]
            assert body["likes"] == test_data["likes"]
            assert body["dislikes"] == test_data["dislikes"]
            assert body["movie_score"] == test_data["movie_score"]
            global REVIEW_ID_TO_DELETE
            REVIEW_ID_TO_DELETE = body["_id"]


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
async def test_create_review_wo_auth(ugc_api_reviews_url, test_data, expected):
    async with ClientSession() as session:
        url = f"{ugc_api_reviews_url}/"

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
async def test_create_review_notok(
    ugc_api_reviews_url, access_token, test_data, expected
):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_reviews_url}/"

        async with session.post(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"


async def test_get_reviews_wo_auth(ugc_api_reviews_url):
    async with ClientSession() as session:
        url = f"{ugc_api_reviews_url}/{MOVIE_ID}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


async def test_get_reviews(ugc_api_reviews_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_reviews_url}/{MOVIE_ID}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert isinstance(body, list)
            assert len(body) >= 0
            assert all([review["_id"] for review in body])
            assert all([review["movie_id"] == MOVIE_ID for review in body])
            assert all([review["user_id"] for review in body])
            assert all([review["text"] for review in body])
            assert all([review["date_published"] for review in body])
            assert all([review["movie_score"] for review in body])
            assert all([review["likes"] for review in body])
            assert all([review["dislikes"] for review in body])


async def test_review_like_wo_auth(ugc_api_reviews_url):
    async with ClientSession() as session:
        url = f"{ugc_api_reviews_url}/{REVIEW_ID_TO_DELETE}/like"

        async with session.post(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


async def test_review_dislike_wo_auth(ugc_api_reviews_url):
    async with ClientSession() as session:
        url = f"{ugc_api_reviews_url}/{REVIEW_ID_TO_DELETE}/dislike"

        async with session.post(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


async def test_delete_review_wo_auth(ugc_api_reviews_url):
    async with ClientSession() as session:
        url = f"{ugc_api_reviews_url}/{REVIEW_ID_TO_DELETE}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


async def test_delete_review_ok_existed(ugc_api_reviews_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_reviews_url}/{REVIEW_ID_TO_DELETE}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert body["deleted_count"] == 1
            assert body["_id"] == REVIEW_ID_TO_DELETE


async def test_delete_review_ok_notexisted(ugc_api_reviews_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_reviews_url}/{REVIEW_ID_TO_DELETE}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert body["deleted_count"] == 0
            assert body["_id"] == REVIEW_ID_TO_DELETE


async def test_delete_review_not_ok(ugc_api_reviews_url, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession(headers=headers) as session:
        url = f"{ugc_api_reviews_url}/qwe"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"
