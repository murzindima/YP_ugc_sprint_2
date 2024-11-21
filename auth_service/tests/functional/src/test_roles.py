import pytest
from aiohttp import ClientSession
from http import HTTPStatus

SUB_PATH = "roles"


@pytest.mark.asyncio
async def test_get_roles(api_base_url, get_jwt_tokens_admin):
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"


@pytest.mark.asyncio
async def test_get_roles_member(api_base_url, get_jwt_tokens_member):
    access_token, _ = get_jwt_tokens_member
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.FORBIDDEN
            ), f"API response status is not {HTTPStatus.FORBIDDEN}"


@pytest.mark.asyncio
async def test_get_roles_no_tokens(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


@pytest.mark.asyncio
async def test_get_roles_refresh_token(api_base_url, get_jwt_tokens_admin):
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
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY},
        ),
    ],
)
@pytest.mark.asyncio
async def test_post_roles(api_base_url, get_jwt_tokens_admin, test_data, expected):
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.post(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"


@pytest.mark.asyncio
async def test_post_roles_no_tokens(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.post(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


@pytest.mark.asyncio
async def test_post_roles_refresh_token(api_base_url, get_jwt_tokens_admin):
    _, refresh_token = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + refresh_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.post(url) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"


@pytest.mark.asyncio
async def test_delete_roles(api_base_url, get_jwt_tokens_admin, get_role_id_member):
    role_id = str(get_role_id_member)
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{role_id}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"


@pytest.mark.asyncio
async def test_delete_roles_wo_id(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.METHOD_NOT_ALLOWED
            ), f"API response status is not {HTTPStatus.METHOD_NOT_ALLOWED}"


@pytest.mark.asyncio
async def test_delete_roles_no_tokens(api_base_url, get_role_id_member):
    role_id = str(get_role_id_member)
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}/{role_id}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


@pytest.mark.asyncio
async def test_delete_roles_refresh_token(
    api_base_url, get_jwt_tokens_admin, get_role_id_member
):
    _, refresh_token = get_jwt_tokens_admin
    role_id = str(get_role_id_member)
    headers = {"Authorization": "Bearer " + refresh_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{role_id}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"


@pytest.mark.asyncio
async def test_patch_roles(api_base_url, get_jwt_tokens_admin, get_role_id_member):
    role_id = str(get_role_id_member)
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{role_id}"

        async with session.patch(url, json={"name": "patched"}) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"


@pytest.mark.asyncio
async def test_patch_roles_wrong_id(api_base_url, get_jwt_tokens_admin):
    role_id = "wrong_id"
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{role_id}"

        async with session.patch(url, json={"name": "patched"}) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"


@pytest.mark.asyncio
async def test_patch_roles_no_tokens(api_base_url, get_role_id_member):
    role_id = str(get_role_id_member)
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}/{role_id}"

        async with session.patch(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


@pytest.mark.asyncio
async def test_patch_roles_refresh_token(
    api_base_url, get_jwt_tokens_admin, get_role_id_member
):
    _, refresh_token = get_jwt_tokens_admin
    role_id = str(get_role_id_member)
    headers = {"Authorization": "Bearer " + refresh_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{role_id}"

        async with session.patch(url) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"
