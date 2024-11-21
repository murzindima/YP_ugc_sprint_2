import pytest
from aiohttp import ClientSession
from http import HTTPStatus

SUB_PATH = "permissions"


@pytest.mark.asyncio
async def test_get_permissions(api_base_url, get_jwt_tokens_admin):
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"


@pytest.mark.asyncio
async def test_get_permissions_member(api_base_url, get_jwt_tokens_member):
    access_token, _ = get_jwt_tokens_member
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.FORBIDDEN
            ), f"API response status is not {HTTPStatus.FORBIDDEN}"


@pytest.mark.asyncio
async def test_get_permissions_no_tokens(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


@pytest.mark.asyncio
async def test_get_permissions_refresh_token(api_base_url, get_jwt_tokens_admin):
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
            {"status": HTTPStatus.CREATED},
        ),
    ],
)
@pytest.mark.asyncio
async def test_post_permissions(
    api_base_url, get_jwt_tokens_admin, test_data, expected
):
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.post(url, json=test_data) as response:
            assert (
                response.status == expected["status"]
            ), f"API response status is not {expected['status']}"
            body = await response.json()
            assert "id" in body
            assert body["name"] == test_data["name"]


@pytest.mark.asyncio
async def test_post_permissions_no_tokens(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.post(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


@pytest.mark.asyncio
async def test_post_permissions_refresh_token(api_base_url, get_jwt_tokens_admin):
    _, refresh_token = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + refresh_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.post(url) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"


@pytest.mark.asyncio
async def test_delete_permissions(
    api_base_url, get_jwt_tokens_admin, create_permission
):
    permission_id, permission_name = create_permission
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{permission_id}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert "id" in body
            assert body["name"] == permission_name


@pytest.mark.asyncio
async def test_delete_permissions_wo_id(api_base_url):
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.METHOD_NOT_ALLOWED
            ), f"API response status is not {HTTPStatus.METHOD_NOT_ALLOWED}"


@pytest.mark.asyncio
async def test_delete_permissions_no_tokens(api_base_url, create_permission):
    permission_id, _ = create_permission
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}/{permission_id}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


@pytest.mark.asyncio
async def test_delete_permissions_refresh_token(
    api_base_url, get_jwt_tokens_admin, create_permission
):
    _, refresh_token = get_jwt_tokens_admin
    permission_id, _ = create_permission
    headers = {"Authorization": "Bearer " + refresh_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{permission_id}"

        async with session.delete(url) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"


@pytest.mark.asyncio
async def test_patch_permissions(api_base_url, get_jwt_tokens_admin, create_permission):
    permission_id, permission_name = create_permission
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{permission_id}"

        async with session.patch(url, json={"name": "patched"}) as response:
            assert (
                response.status == HTTPStatus.OK
            ), f"API response status is not {HTTPStatus.OK}"
            body = await response.json()
            assert "id" in body
            assert body["name"] == "patched"


@pytest.mark.asyncio
async def test_patch_permissions_wrong_id(api_base_url, get_jwt_tokens_admin):
    permission_id = "wrong_id"
    access_token, _ = get_jwt_tokens_admin
    headers = {"Authorization": "Bearer " + access_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{permission_id}"

        async with session.patch(url, json={"name": "patched"}) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"


@pytest.mark.asyncio
async def test_patch_permissions_no_tokens(api_base_url, create_permission):
    permission_id, _ = create_permission
    async with ClientSession() as session:
        url = f"{api_base_url}/{SUB_PATH}/{permission_id}"

        async with session.patch(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"


@pytest.mark.asyncio
async def test_patch_permissions_refresh_token(
    api_base_url, get_jwt_tokens_admin, create_permission
):
    _, refresh_token = get_jwt_tokens_admin
    permission_id, _ = create_permission
    headers = {"Authorization": "Bearer " + refresh_token}
    async with ClientSession(headers=headers) as session:
        url = f"{api_base_url}/{SUB_PATH}/{permission_id}"

        async with session.patch(url) as response:
            assert (
                response.status == HTTPStatus.UNPROCESSABLE_ENTITY
            ), f"API response status is not {HTTPStatus.UNPROCESSABLE_ENTITY}"
