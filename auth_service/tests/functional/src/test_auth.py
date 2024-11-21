import pytest
from aiohttp import ClientSession
from http import HTTPStatus
from tests.functional.fixtures.common import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    MEMBER_PASSWORD,
    MEMBER_EMAIL,
    MEMBER_FIRST_NAME,
    MEMBER_LAST_NAME,
)

SUB_PATH = "auth"


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (
            {
                "email": "some@email.com",
                "password": MEMBER_PASSWORD,
                "first_name": MEMBER_FIRST_NAME,
                "last_name": MEMBER_LAST_NAME,
            },
            {"status": HTTPStatus.CREATED},
        ),
    ],
)
@pytest.mark.asyncio
async def test_signup_member(api_base_url, get_role_id_member, test_data, expected):
    test_data["role_id"] = str(get_role_id_member)
    # TODO FIX admin signup
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}/signup"
        async with session.post(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"
            body = await response.json()
            assert "id" in body
            assert body["first_name"] == test_data["first_name"]
            assert body["last_name"] == test_data["last_name"]
            assert body["role_id"] == test_data["role_id"]


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (
            {
                "email": MEMBER_EMAIL,
                "password": MEMBER_PASSWORD,
                "first_name": MEMBER_FIRST_NAME,
                "last_name": MEMBER_LAST_NAME,
            },
            {"status": HTTPStatus.FORBIDDEN},
        ),
    ],
)
@pytest.mark.asyncio
async def test_signup_restricted_roles(
    api_base_url, get_role_id_privileged, test_data, expected
):
    test_data["role_id"] = str(get_role_id_privileged)
    # TODO FIX admin signup
    test_data["email"] = f"{test_data['role_id'][0]}{test_data['email']}"
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}/signup"
        async with session.post(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (
            {
                "email": "some@email.com",
                "password": MEMBER_PASSWORD,
                "first_name": MEMBER_FIRST_NAME,
                "last_name": MEMBER_LAST_NAME,
            },
            {"status": HTTPStatus.UNAUTHORIZED},
        ),
        (
            {
                "email": "toooooooooooooooooooooooooooooooooooolooooedddddddddddooooooooongeeeemmmaaaaail@example.com",
                "password": MEMBER_PASSWORD,
                "first_name": MEMBER_FIRST_NAME,
                "last_name": MEMBER_LAST_NAME,
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        (
            {
                "email": "email@mail.com",
                "password": MEMBER_PASSWORD,
                "first_name": MEMBER_FIRST_NAME,
                "last_name": MEMBER_LAST_NAME,
                "role_id": "1234567890",
            },
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
    ],
)
@pytest.mark.asyncio
async def test_signup_422(api_base_url, get_role_id_member, test_data, expected):
    role_id = test_data.get("role_id", None)
    if role_id is None:
        test_data["role_id"] = str(get_role_id_member)
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}/signup"
        async with session.post(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"


@pytest.mark.asyncio
async def test_login(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}/login"

        async with session.post(
            url, json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
        ) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert "access_token" in body
            assert "refresh_token" in body


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (
            {"email": MEMBER_EMAIL, "password": "123qwe"},
            {"status": HTTPStatus.UNAUTHORIZED},
        ),
        (
            {"email": "a@b.c", "password": MEMBER_PASSWORD},
            {"status": HTTPStatus.UNAUTHORIZED},
        ),
        (
            {"email": "a@b", "password": MEMBER_PASSWORD},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
        ({"email": "", "password": ""}, {"status": HTTPStatus.UNPROCESSABLE_ENTITY}),
        ({"email": ""}, {"status": HTTPStatus.UNPROCESSABLE_ENTITY}),
        ({"password": ""}, {"status": HTTPStatus.UNPROCESSABLE_ENTITY}),
        ({}, {"status": HTTPStatus.UNPROCESSABLE_ENTITY}),
    ],
)
@pytest.mark.asyncio
async def test_login_fail(api_base_url, test_data, expected):
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}/login"

        async with session.post(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"


@pytest.mark.asyncio
async def test_login_no_body(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}/login"

        async with session.post(url) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"


@pytest.mark.asyncio
async def test_logout(api_base_url, get_jwt_tokens_admin):
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/logout"

        async with session.post(url) as response:
            assert (
                response.status == HTTPStatus.NO_CONTENT
            ), f"API response status is not {HTTPStatus.NO_CONTENT}"


@pytest.mark.asyncio
async def test_logout_refresh(api_base_url, get_jwt_tokens_admin):
    _, refresh_token = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + refresh_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/logout"

        async with session.post(url) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"


@pytest.mark.asyncio
async def test_logout_both_tokens(api_base_url, get_jwt_tokens_admin):
    access_token, refresh_token = get_jwt_tokens_admin
    headers = {
        "Authorization": "Bearer " + access_token,
        "Authorization": "Bearer " + refresh_token,
    }
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/logout"

        async with session.post(url) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"


@pytest.mark.asyncio
async def test_logout_fail(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}/logout"

        async with session.post(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


@pytest.mark.asyncio
async def test_refresh_tokens(api_base_url, get_jwt_tokens_admin):
    _, refresh_token = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + refresh_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/refresh-tokens"

        async with session.post(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert "access_token" in body
            assert "refresh_token" in body


@pytest.mark.asyncio
async def test_refresh_tokens_access(api_base_url, get_jwt_tokens_admin):
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/refresh-tokens"

        async with session.post(url) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"


@pytest.mark.asyncio
async def test_refresh_tokens_both(api_base_url, get_jwt_tokens_admin):
    access_token, refresh_token = get_jwt_tokens_admin
    headers = {
        "Authorization": "Bearer " + access_token,
        "Authorization": "Bearer " + refresh_token,
    }
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/refresh-tokens"

        async with session.post(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"


@pytest.mark.asyncio
async def test_refresh_tokens_fail(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}/refresh-tokens"

        async with session.post(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"
