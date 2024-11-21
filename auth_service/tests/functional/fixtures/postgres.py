import pytest
import pytest_asyncio
from sqlalchemy import select, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.models.role import Role, RoleType
from src.tools.init_db import (
    _create_permissions,
    _create_roles,
    _assign_permissions_to_roles,
    _create_admin,
)
from src.db.postgres import create_database, purge_database, dsn
from tests.functional.fixtures.common import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    ADMIN_FIRST_NAME,
    ADMIN_LAST_NAME,
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def pg_init():
    await purge_database()
    await create_database()
    await _create_permissions()
    await _create_roles()
    await _assign_permissions_to_roles()
    await _create_admin(
        email=ADMIN_EMAIL,
        password=ADMIN_PASSWORD,
        first_name=ADMIN_FIRST_NAME,
        last_name=ADMIN_LAST_NAME,
    )


@pytest.fixture(scope="session")
def pg_async_session():
    _engine = create_async_engine(dsn, echo=True, future=True, poolclass=NullPool)
    async_session = sessionmaker(
        _engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return async_session


@pytest_asyncio.fixture(
    params=[
        RoleType.MEMBER.value,
        RoleType.ADMIN.value,
        RoleType.MODERATOR.value,
        RoleType.SUBSCRIBER.value,
    ]
)
async def get_role_id_all(pg_async_session, request):
    async with pg_async_session() as session:
        result = await session.execute(select(Role).where(Role.name == request.param))
        role = result.unique().scalar_one_or_none()
        yield role.id if role else None


@pytest_asyncio.fixture(
    params=[RoleType.ADMIN.value, RoleType.MODERATOR.value, RoleType.SUBSCRIBER.value]
)
async def get_role_id_privileged(pg_async_session, request):
    async with pg_async_session() as session:
        result = await session.execute(select(Role).where(Role.name == request.param))
        role = result.unique().scalar_one_or_none()
        yield role.id if role else None


@pytest_asyncio.fixture(params=[RoleType.MEMBER.value])
async def get_role_id_member(pg_async_session, request):
    async with pg_async_session() as session:
        result = await session.execute(select(Role).where(Role.name == request.param))
        role = result.unique().scalar_one_or_none()
        yield role.id if role else None
