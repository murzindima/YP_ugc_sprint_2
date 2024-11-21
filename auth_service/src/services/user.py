from functools import lru_cache
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.messages import ROLE_NOT_FOUND, USER_ALREADY_EXISTS, FORBIDDEN_OPERATION
from src.db.postgres import get_session
from src.models.role import RoleType
from src.models.user import User as UserModel
from src.schemas.login_history import LoginHistory as LoginHistorySchema
from src.schemas.user import User as UserSchema
from src.schemas.user import UserCreate as UserCreateSchema
from src.schemas.user import UserUpdate as UserUpdateSchema
from src.services.base import BaseService
from src.services.data_repository.postgres import PostgresService


class UserService(BaseService):
    """Service class for managing users, extending the BaseService."""

    async def get_login_history(
        self, user_id: UUID, page: int, size: int
    ) -> list[LoginHistorySchema]:
        """Validate user's login history."""
        db_models = await self.postgres_service.get_login_history(
            user_id=user_id, page=page, size=size
        )
        return [LoginHistorySchema.model_validate(model) for model in db_models]

    async def create_user(self, new_user: UserCreateSchema) -> UserSchema:
        """Create a new user."""
        existing_user = await self.postgres_service.get_user_by_email(new_user.email)
        if existing_user:
            raise HTTPException(
                detail=USER_ALREADY_EXISTS, status_code=status.HTTP_401_UNAUTHORIZED
            )

        requested_role = await self.postgres_service.get_role(role_id=new_user.role_id)
        if not requested_role:
            raise HTTPException(
                detail=ROLE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND
            )

        if requested_role.name != RoleType.MEMBER:
            raise HTTPException(
                detail=FORBIDDEN_OPERATION, status_code=status.HTTP_403_FORBIDDEN
            )

        return await super().create_model(new_user)

    async def update_user(
        self, user_id: UUID, new_user_data: UserUpdateSchema
    ) -> UserSchema | None:
        """Update an existing user."""
        if new_user_data.role_id:
            requested_role = await self.postgres_service.get_role(
                role_id=new_user_data.role_id
            )
            if not requested_role:
                raise HTTPException(
                    detail=ROLE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND
                )

        return await super().update_model(model_id=user_id, new_data=new_user_data)


@lru_cache
def get_user_service(pg_session: AsyncSession = Depends(get_session)) -> UserService:
    """Dependency function to get an instance of the UserService."""
    return UserService(
        model_schema_class=UserSchema,
        postgres_service=PostgresService(session=pg_session, model_class=UserModel),
    )
