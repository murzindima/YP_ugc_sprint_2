from uuid import UUID

from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from src.core.messages import NOT_AUTHENTICATED
from src.db.postgres import get_session
from src.db.redis import get_redis
from src.models.user import User as UserModel
from src.schemas.user import User as UserSchema
from src.services.data_repository.postgres import PostgresService


class AccessJWTBearer(HTTPBearer):
    """Middleware for handling JWT authentication."""

    def __init__(self, auto_error: bool = True):
        """Initialize the JWTBearer middleware."""
        super().__init__(auto_error=auto_error)

    async def __call__(
        self,
        request: Request,
        session: AsyncSession = Depends(get_session),
        redis: Redis = Depends(get_redis),
    ) -> UserModel | None:
        """Handle incoming requests and perform JWT authentication."""
        authorize = AuthJWT(req=request)
        await authorize.jwt_optional()

        user_id = await authorize.get_jwt_subject()
        if not user_id:
            return None

        user = await PostgresService(session=session, model_class=UserModel).get_by_id(
            model_id=UUID(user_id)
        )
        if not user:
            return None

        return user


async def set_current_user(
    request: Request, user: UserModel | None = Depends(AccessJWTBearer())
) -> None:
    """Set the authenticated user data in the request object."""
    setattr(request, "user_data", user)


async def get_current_user(
    user: UserModel | None = Depends(AccessJWTBearer()),
) -> UserSchema:
    """Get the authenticated user data from the request object."""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=NOT_AUTHENTICATED
        )

    return UserSchema.model_validate(user)
