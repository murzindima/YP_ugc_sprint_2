from fastapi import APIRouter, Depends, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from src.middleware.access_jwt import AccessJWTBearer
from src.middleware.access_jwt import set_current_user as set_current_user_access_jwt
from src.middleware.refresh_jwt import set_current_user as set_current_user_refresh_jwt
from src.schemas.auth import TokenPair as TokenPairSchema
from src.schemas.user import User as UserSchema
from src.schemas.user import UserCreate as UserCreateSchema
from src.schemas.user import UserLogin as UserLoginSchema
from src.services.auth import AuthService, get_auth_service
from src.services.user import UserService, get_user_service

router = APIRouter()


@router.post(
    "/signup",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AccessJWTBearer())],
)
async def create_user(
    user_data: UserCreateSchema,
    user_service: UserService = Depends(get_user_service),
) -> UserSchema:
    """Creates a new user."""
    user = await user_service.create_user(user_data)
    return user


@router.post(
    "/login",
    response_model=TokenPairSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AccessJWTBearer())],
)
async def login(
    user_data: UserLoginSchema,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenPairSchema:
    """Logs in the user by exchanging the user's credentials for two tokens."""
    tokens = await auth_service.login(**user_data.model_dump(), request=request)
    return tokens


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(set_current_user_access_jwt)],
)
async def logout(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> None:
    """Logs out the user."""
    await auth_service.logout(request)


@router.post(
    "/refresh-tokens",
    response_model=TokenPairSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(set_current_user_refresh_jwt)],
)
async def refresh_tokens(
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenPairSchema:
    """Updates the user's tokens by the refresh token."""
    tokens = await auth_service.refresh_tokens()
    return tokens


@router.get("/login/oauth/{provider}", status_code=status.HTTP_302_FOUND)
async def oauth_login(
    provider: str, auth_service: AuthService = Depends(get_auth_service)
):
    """Redirects the user to the OAuth provider's login page."""
    authorization_url = await auth_service.get_authorization_url(provider)
    return RedirectResponse(url=authorization_url)


@router.get(
    "/login/oauth/{provider}/callback",
    response_model=TokenPairSchema,
    status_code=status.HTTP_200_OK,
)
async def oauth_callback(
    provider: str,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Handles the OAuth provider's callback."""
    tokens = await auth_service.process_oauth_callback(provider, request)
    return tokens
