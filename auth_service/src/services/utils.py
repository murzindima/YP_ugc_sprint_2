from functools import wraps

import jwt
from fastapi import HTTPException, status

from src.core.config import app_settings
from src.core.messages import FORBIDDEN_OPERATION, REQUEST_NOT_FOUND
from src.models.role import RoleType
from src.models.user import User as UserModel


async def get_token_jti(token: str) -> str | None:
    """Decode the JWT token and retrieve the JWT ID."""
    decoded_token = jwt.decode(
        token, key=app_settings.authjwt_secret_key, algorithms=["HS256"]
    )
    token_jti = decoded_token.get("jti")
    return token_jti


def roles_required(roles_list: list[RoleType]):
    """Decorator to restrict access to a FastAPI endpoint based on user roles list."""

    def decorator(function):
        @wraps(function)
        async def wrapper(*args, **kwargs):
            """Wrapper function to perform roles-based access control."""
            request = kwargs.get("request")
            if not request:
                raise HTTPException(
                    detail=REQUEST_NOT_FOUND,
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            user: UserModel = request.user_data
            if not user or user.role.name not in [role for role in roles_list]:
                raise HTTPException(
                    detail=FORBIDDEN_OPERATION, status_code=status.HTTP_403_FORBIDDEN
                )

            return await function(*args, **kwargs)

        return wrapper

    return decorator


requires_admin = roles_required(roles_list=[RoleType.ADMIN])
