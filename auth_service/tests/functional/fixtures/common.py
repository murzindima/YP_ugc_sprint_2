import uuid

import pytest
import pytest_asyncio
from aiohttp import ClientSession

from tests.functional.settings import test_settings

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "sup3rp@ssw0rd"
ADMIN_FIRST_NAME = "Admin"
ADMIN_LAST_NAME = "Admin"
MEMBER_EMAIL = "member@example.com"
MEMBER_PASSWORD = "sup3rp@ssw0rd"
MEMBER_FIRST_NAME = "Member"
MEMBER_LAST_NAME = "Member"
MODERATOR_EMAIL = "moderator@example.com"
MODERATOR_PASSWORD = "sup3rp@ssw0rd"
MODERATOR_FIRST_NAME = "Moderator"
MODERATOR_LAST_NAME = "Moderator"
SUBSCRIBER_EMAIL = "subscriber@example.com"
SUBSCRIBER_PASSWORD = "sup3rp@ssw0rd"
SUBSCRIBER_FIRST_NAME = "Subscriber"
SUBSCRIBER_LAST_NAME = "Subscriber"


@pytest.fixture
def api_base_url():
    api_url = test_settings.api_url
    base_path = test_settings.api_base_path
    base_url = f"{api_url}{base_path}"
    return base_url


@pytest_asyncio.fixture
async def get_jwt_tokens_admin(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/auth/login"

        async with session.post(
            url, json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
        ) as response:
            body = await response.json()
            access_token = body["access_token"]
            refresh_token = body["refresh_token"]
            return access_token, refresh_token


@pytest_asyncio.fixture
async def create_permission(api_base_url, get_jwt_tokens_admin):
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}

    random_name = "permission_" + uuid.uuid4().hex

    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/permissions"
        async with session.post(url, json={"name": random_name}) as response:
            body = await response.json()
            permission_id = body["id"]
            permission_name = body["name"]

    return permission_id, permission_name


@pytest_asyncio.fixture
async def create_user(api_base_url, get_role_id_member):
    role_id = str(get_role_id_member)
    email = uuid.uuid4().hex + "@example.com"
    json = {
        "email": email,
        "password": MEMBER_PASSWORD,
        "first_name": MEMBER_FIRST_NAME,
        "last_name": MEMBER_LAST_NAME,
        "role_id": role_id,
    }
    async with ClientSession() as session:
        url = f"{api_base_url}/auth/signup"
        async with session.post(url, json=json) as response:
            body = await response.json()
            _id = body["id"]
            _role_id = body["role_id"]
            return _id, _role_id, email


@pytest_asyncio.fixture
async def signup_member(api_base_url, get_role_id_member):
    role_id = str(get_role_id_member)
    json = {
        "email": MEMBER_EMAIL,
        "password": MEMBER_PASSWORD,
        "first_name": MEMBER_FIRST_NAME,
        "last_name": MEMBER_LAST_NAME,
        "role_id": role_id,
    }
    try:
        async with ClientSession() as session:
            url = f"{api_base_url}/auth/signup"
            async with session.post(url, json=json) as response:
                body = await response.json()
                _id = body["id"]
                _role_id = body["role_id"]
                return _id, _role_id
    except Exception:
        pass


@pytest_asyncio.fixture
async def get_jwt_tokens_member(api_base_url, signup_member):
    async with ClientSession() as session:
        url = f"{api_base_url}/auth/login"

        async with session.post(
            url, json={"email": MEMBER_EMAIL, "password": MEMBER_PASSWORD}
        ) as response:
            body = await response.json()
            access_token = body["access_token"]
            refresh_token = body["refresh_token"]
            return access_token, refresh_token
