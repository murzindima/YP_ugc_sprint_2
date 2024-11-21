from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status, Query

from src.core.config import app_settings
from src.core.messages import FORBIDDEN_OPERATION, USER_NOT_FOUND
from src.middleware.access_jwt import get_current_user
from src.models.role import RoleType
from src.schemas.login_history import LoginHistory as LoginHistorySchema
from src.schemas.user import User as UserSchema
from src.schemas.user import UserUpdate as UserUpdateSchema
from src.services.auth import AuthService, get_auth_service
from src.services.role import RoleService, get_role_service
from src.services.user import UserService, get_user_service
from src.services.utils import requires_admin

router = APIRouter()


@router.get("", response_model=list[UserSchema], status_code=status.HTTP_200_OK)
@requires_admin
async def get_users(
    request: Request,
    user_service: UserService = Depends(get_user_service),
) -> list[UserSchema]:
    """Returns multiple users."""
    users = await user_service.get_all_models()
    return users


@router.get("/{user_id}", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
) -> UserSchema:
    """Returns a user by identifier."""
    user = await user_service.get_model_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
        )

    return user


@router.get(
    "/{user_id}/login-history",
    response_model=list[LoginHistorySchema],
    status_code=status.HTTP_200_OK,
)
async def get_user_login_history(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service),
    current_user: UserSchema = Depends(get_current_user),
    page: int = Query(1, ge=1),
    size: int = Query(app_settings.pagination_size, ge=1),
) -> list[LoginHistorySchema]:
    """Returns the user's login history."""
    permission = (
        "VIEW OWN LOGIN_HISTORY"
        if current_user.id == user_id
        else "VIEW OTHER LOGIN_HISTORY"
    )
    await auth_service.check_permission(permission=permission, user_id=current_user.id)
    login_history = await user_service.get_login_history(
        user_id=user_id, page=page, size=size
    )
    return login_history


@router.patch("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: UUID,
    new_data: UserUpdateSchema,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service),
    role_service: RoleService = Depends(get_role_service),
    current_user: UserSchema = Depends(get_current_user),
) -> UserSchema:
    """Updates a user by identifier."""
    permission = "EDIT OWN USER" if current_user.id == user_id else "EDIT OTHER USER"
    await auth_service.check_permission(permission=permission, user_id=current_user.id)

    user_role = await role_service.get_model_by_id(current_user.role_id)
    if new_data.role_id and user_role.name != RoleType.ADMIN:
        raise HTTPException(
            detail=FORBIDDEN_OPERATION, status_code=status.HTTP_403_FORBIDDEN
        )

    user = await user_service.update_user(user_id=user_id, new_user_data=new_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
        )

    return user
