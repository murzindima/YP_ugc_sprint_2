import pytest
import pytest_asyncio
from aiohttp import ClientSession

from tests.functional.settings import test_settings


EMAIL = "a@b.com"
PASSWORD = "123qwe"
USER_ID = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
MOVIE_ID = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
BOOKMARKS_SUB_PATH = "bookmarks"
LIKES_SUB_PATH = "likes"
REVIEWS_SUB_PATH = "reviews"


@pytest.fixture
def ugc_api_bookmarks_url():
    return f"{test_settings.ugc_api_url}/{BOOKMARKS_SUB_PATH}"


@pytest.fixture
def ugc_api_likes_url():
    return f"{test_settings.ugc_api_url}/{LIKES_SUB_PATH}"


@pytest.fixture
def ugc_api_reviews_url():
    return f"{test_settings.ugc_api_url}/{REVIEWS_SUB_PATH}"


@pytest_asyncio.fixture(scope="session")
async def access_token():
    async with ClientSession() as session:
        url = f"{test_settings.auth_api_url}/auth/login"

        async with session.post(
            url, json={"email": EMAIL, "password": PASSWORD}
        ) as response:
            body = await response.json()
            access_token = body["access_token"]
            return access_token
