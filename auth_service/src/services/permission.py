from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_session
from src.models.permission import Permission as PermissionModel
from src.schemas.permission import Permission as PermissionSchema
from src.services.base import BaseService
from src.services.data_repository.postgres import PostgresService


class PermissionService(BaseService):
    """Service class for managing permissions, extending the BaseService."""


@lru_cache
def get_permission_service(
    pg_session: AsyncSession = Depends(get_session),
) -> PermissionService:
    """Dependency function to get an instance of the PermissionService."""
    return PermissionService(
        model_schema_class=PermissionSchema,
        postgres_service=PostgresService(
            session=pg_session, model_class=PermissionModel
        ),
    )
