from uuid import UUID

from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from starlette import status
from starlette.requests import Request

from src.core.messages import NOT_AUTHENTICATED


class JWTBearer(HTTPBearer):
    """Middleware for handling JWT authentication."""

    def __init__(self, auto_error: bool = True):
        """Initialize the JWTBearer middleware."""
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> UUID:
        """Handle incoming requests and perform JWT authentication."""
        authorize = AuthJWT(req=request)
        await authorize.jwt_required()

        user_jwt: str = await authorize.get_jwt_subject()
        try:
            user_jwt: UUID = UUID(user_jwt)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=NOT_AUTHENTICATED
            )

        return user_jwt


async def set_current_user(
    request: Request, user_jwt: UUID = Depends(JWTBearer())
) -> None:
    """Set the authenticated user data in the request object."""
    setattr(request, "user_jwt", user_jwt)
