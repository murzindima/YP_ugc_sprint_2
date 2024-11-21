from uuid import UUID

from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends
from fastapi.security import HTTPBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.db.postgres import get_session
from src.db.redis import get_redis
from src.models.user import User as UserModel
from src.services.data_repository.postgres import PostgresService


class RefreshJWTBearer(HTTPBearer):
    """Middleware for handling refresh JWT authentication."""

    def __init__(self, auto_error: bool = True):
        """Initialize the RefreshJWTBearer middleware."""
        super().__init__(auto_error=auto_error)

    async def __call__(
        self,
        request: Request,
        session: AsyncSession = Depends(get_session),
        redis: Redis = Depends(get_redis),
    ) -> UserModel | None:
        """Handle incoming requests and perform refresh JWT authentication."""
        authorize = AuthJWT(req=request)
        await authorize.jwt_refresh_token_required()

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
    request: Request, user: UserModel | None = Depends(RefreshJWTBearer())
) -> None:
    """Set the authenticated user data in the request object."""
    setattr(request, "user_data", user)
