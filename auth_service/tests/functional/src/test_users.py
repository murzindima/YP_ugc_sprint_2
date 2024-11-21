import pytest
from aiohttp import ClientSession
from http import HTTPStatus

from tests.functional.fixtures.common import MEMBER_PASSWORD

SUB_PATH = "users"


@pytest.mark.asyncio
async def test_get_users(api_base_url, get_jwt_tokens_admin):
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"


@pytest.mark.asyncio
async def test_get_users_member(api_base_url, get_jwt_tokens_member):
    access_token, _ = get_jwt_tokens_member
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.FORBIDDEN
            ), f"API response status is not {HTTPStatus.FORBIDDEN}"


@pytest.mark.asyncio
async def test_get_user_by_admin(api_base_url, get_jwt_tokens_admin, create_user):
    user_id, role_id, _ = create_user
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{user_id}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert body["id"] == user_id
            assert body["role_id"] == role_id
            assert "first_name" in body
            assert "last_name" in body


@pytest.mark.asyncio
async def test_get_user_by_random_member(
    api_base_url, get_jwt_tokens_member, create_user
):
    user_id, role_id, _ = create_user
    access_token, _ = get_jwt_tokens_member
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{user_id}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert body["id"] == user_id
            assert body["role_id"] == role_id
            assert "first_name" in body
            assert "last_name" in body


@pytest.mark.asyncio
async def test_get_user_by_member(api_base_url, create_user):
    user_id, role_id, email = create_user
    async with ClientSession() as session:
        url = f"{api_base_url}/auth/login"
        async with session.post(
            url, json={"email": email, "password": MEMBER_PASSWORD}
        ) as response:
            body = await response.json()
            access_token = body["access_token"]
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{user_id}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert body["id"] == user_id
            assert body["role_id"] == role_id
            assert "first_name" in body
            assert "last_name" in body


@pytest.mark.asyncio
async def test_get_users_no_tokens(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


@pytest.mark.asyncio
async def test_get_users_refresh_token(api_base_url, get_jwt_tokens_admin):
    _, refresh_token = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + refresh_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (
            {
                "name": "test",
            },
            {"status": HTTPStatus.METHOD_NOT_ALLOWED},
        ),
    ],
)
@pytest.mark.asyncio
async def test_post_users(api_base_url, get_jwt_tokens_admin, test_data, expected):
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.post(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"


@pytest.mark.asyncio
async def test_post_users_no_tokens(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.post(url) as response:
            assert (
                response.status == HTTPStatus.METHOD_NOT_ALLOWED
            ), f"API response status is not {HTTPStatus.METHOD_NOT_ALLOWED}"


@pytest.mark.asyncio
async def test_post_users_refresh_token(api_base_url, get_jwt_tokens_admin):
    _, refresh_token = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + refresh_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.post(url) as response:
            assert (
                response.status == HTTPStatus.METHOD_NOT_ALLOWED
            ), f"API response status is not {HTTPStatus.METHOD_NOT_ALLOWED}"


@pytest.mark.asyncio
async def test_delete_user(api_base_url, get_jwt_tokens_admin):
    user_id = "1234567890"
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{user_id}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.METHOD_NOT_ALLOWED
            ), f"API response status is not {HTTPStatus.METHOD_NOT_ALLOWED}"


@pytest.mark.asyncio
async def test_patch_user(api_base_url, get_jwt_tokens_admin, create_user):
    user_id, _, _ = create_user
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{user_id}"

        async with session.patch(url, json={"first_name": "patched"}) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert body["first_name"] == "patched"


@pytest.mark.asyncio
async def test_patch_user_wrong_role_id(
    api_base_url, get_jwt_tokens_admin, create_user
):
    user_id, _, _ = create_user
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{user_id}"

        async with session.patch(url, json={"role_id": "patched"}) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"


@pytest.mark.asyncio
async def test_patch_user_wrong_user_id(api_base_url, get_jwt_tokens_admin):
    user_id = "wrong_id"
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{user_id}"

        async with session.patch(url, json={"first_name": "patched"}) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"


@pytest.mark.asyncio
async def test_patch_user_no_tokens(api_base_url, create_user):
    user_id, _, _ = create_user
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}/{user_id}"

        async with session.patch(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


@pytest.mark.asyncio
async def test_patch_user_refresh_token(
    api_base_url, get_jwt_tokens_admin, create_user
):
    _, refresh_token = get_jwt_tokens_admin
    user_id, _, _ = create_user
    headers = {"Authorization": "Bearer " + refresh_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{user_id}"

        async with session.patch(url) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"
