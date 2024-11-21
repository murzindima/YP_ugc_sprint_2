from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_session
from src.models.role import Role as RoleModel
from src.schemas.role import Role as RoleSchema
from src.services.base import BaseService
from src.services.data_repository.postgres import PostgresService


class RoleService(BaseService):
    """Service class for managing roles, extending the BaseService."""


@lru_cache
def get_role_service(pg_session: AsyncSession = Depends(get_session)) -> RoleService:
    """Dependency function to get an instance of the RoleService."""
    return RoleService(
        model_schema_class=RoleSchema,
        postgres_service=PostgresService(session=pg_session, model_class=RoleModel),
    )
