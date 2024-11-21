from datetime import timedelta, datetime
from functools import lru_cache
from uuid import UUID

from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException, Request
from pydantic import EmailStr
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from werkzeug.security import check_password_hash
from yandexid import AsyncYandexOAuth, AsyncYandexID

from src.core.config import app_settings, oauth2_settings
from src.core.messages import (
    FORBIDDEN_OPERATION,
    INCORRECT_PASSWORD_OR_EMAIL,
    REFRESH_TOKEN_HAS_BEEN_REVOKED,
)
from src.db.postgres import get_session
from src.db.redis import get_redis
from src.models.oauth_provider import OAuthProvider
from src.schemas.auth import OAuthProviderCreate
from src.models.role import RoleType
from src.models.user import User as UserModel
from src.schemas.auth import TokenPair as TokenPairSchema
from src.schemas.user import UserCreate
from src.services.abstract.auth import AuthAbstractService
from src.services.data_repository.postgres import PostgresService
from src.services.data_repository.redis_cache import RedisCacheService
from src.services.user import UserService
from src.services.utils import get_token_jti


class AuthService(AuthAbstractService):
    """Service for handling user authentication."""

    def __init__(
        self,
        user_service: UserService,
        postgres_service: PostgresService,
        redis_service: RedisCacheService,
        auth_jwt: AuthJWT,
    ):
        self.user_service = user_service
        self.postgres_service = postgres_service
        self.redis_service = redis_service
        self.auth_jwt = auth_jwt
        self.oauth = AsyncYandexOAuth(
            client_id=oauth2_settings.client_id,
            client_secret=oauth2_settings.client_secret,
            redirect_uri=oauth2_settings.redirect_uri,
        )

    async def login(
        self, email: EmailStr, password: str, request: Request
    ) -> TokenPairSchema:
        """Generate access and refresh tokens."""
        user = await self.postgres_service.get_user_by_email(email=email)

        if not user or not check_password_hash(user.password, password):
            raise HTTPException(
                detail=INCORRECT_PASSWORD_OR_EMAIL,
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        tokens: TokenPairSchema = await self._create_tokens(user)

        refresh_token_jti = await get_token_jti(tokens.refresh_token)
        await self.postgres_service.create_login_history(
            user_id=user.id,
            ip_address=request.client.host,
            refresh_token=refresh_token_jti,
        )

        return tokens

    async def logout(self, request: Request) -> None:
        """Log out the user and make the access token expired."""
        await self.auth_jwt.jwt_required()

        raw_jwt = await self.auth_jwt.get_raw_jwt()
        access_token_jti = raw_jwt["jti"]
        await self.redis_service.put_to_cache(access_token_jti, "true")

        user_id = raw_jwt["sub"]
        await self.postgres_service.deactivate_from_user_history(
            user_id=UUID(user_id), current_user_ip_address=request.client.host
        )

    async def refresh_tokens(self) -> TokenPairSchema:
        """Refresh tokens of the user."""
        user_id = await self.auth_jwt.get_jwt_subject()
        token = await self.auth_jwt.get_raw_jwt()
        token_jti = token.get("jti")
        user = await self.postgres_service.get_by_id(UUID(user_id))

        db_models = await self.postgres_service.get_login_history(
            user_id=UUID(user_id), refresh_token=token_jti
        )
        if not token_jti or not user or not db_models or not db_models[0].is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=REFRESH_TOKEN_HAS_BEEN_REVOKED,
            )

        tokens: TokenPairSchema = await self._create_tokens(user)
        refresh_token_jti = await get_token_jti(tokens.refresh_token)
        await self.postgres_service.update_user_history(
            user_id=UUID(user_id),
            refresh_token=refresh_token_jti,
        )
        return tokens

    async def _create_tokens(self, user: UserModel) -> TokenPairSchema:
        """Create both tokens for a user."""
        access_token = await self.auth_jwt.create_access_token(
            subject=str(user.id),
            expires_time=app_settings.access_token_expires,
            user_claims={"role": str(user.role.name)},
        )
        refresh_token = await self.auth_jwt.create_refresh_token(
            subject=str(user.id),
            expires_time=app_settings.refresh_token_expires,
            user_claims={"role": str(user.role.name)},
        )
        return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)

    async def check_permission(self, permission: str, user_id: UUID) -> None:
        """Check user's permission."""
        user = await self.postgres_service.get_by_id(user_id)
        if not any(
            role_permission.permission.name == permission
            for role_permission in user.role.permissions
        ):
            raise HTTPException(
                detail=FORBIDDEN_OPERATION, status_code=status.HTTP_403_FORBIDDEN
            )

    async def get_authorization_url(self, provider: str = "yandex") -> str:
        """Generate the URL to redirect the user to the OAuth provider's login page."""
        if provider != "yandex":  # TODO: Add more providers
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported provider"
            )

        return self.oauth.get_authorization_url()

    async def process_oauth_callback(
        self, provider: str, request: Request
    ) -> TokenPairSchema:
        """Process the callback from the OAuth provider and return user information."""
        token = await self.oauth.get_token_from_code(request.query_params["code"])
        access_token = token.access_token
        refresh_token = token.refresh_token
        yandex_id = AsyncYandexID(access_token)
        user_info = await yandex_id.get_user_info_json()
        provider_user_id = user_info.id
        email = user_info.default_email
        oauth_provider = await self.postgres_service.get_oauth_provider(
            provider_name=provider, provider_user_id=provider_user_id
        )
        if oauth_provider:
            user = oauth_provider.user
        else:
            user = await self.postgres_service.get_user_by_email(email=email)
            if not user:
                role_id = await self.postgres_service.get_role_id_by_name(
                    RoleType.MEMBER
                )
                new_user_model = UserCreate(
                    email=email,
                    first_name=user_info.first_name,
                    last_name=user_info.last_name,
                    role_id=str(role_id),
                )
                user = await self.postgres_service.create(new_user_model)
            token_expires_at = datetime.utcnow() + timedelta(seconds=token.expires_in)
            oauth_provider = OAuthProviderCreate(
                provider_name=provider,
                provider_user_id=provider_user_id,
                user_id=user.id,
                access_token=access_token,
                refresh_token=refresh_token,
                token_expires_at=token_expires_at,
            )
            _postgres_service = PostgresService(
                session=self.postgres_service.session, model_class=OAuthProvider
            )
            await _postgres_service.create(oauth_provider)

        tokens: TokenPairSchema = await self._create_tokens(user)
        refresh_token_jti = await get_token_jti(tokens.refresh_token)
        await self.postgres_service.update_user_history(
            user_id=user.id,
            refresh_token=refresh_token_jti,
        )
        return tokens


@lru_cache
def get_auth_service(
    pg_session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
    auth_jwt: AuthJWT = Depends(),
) -> AuthService:
    """Dependency function to get an instance of the AuthService."""
    return AuthService(
        user_service=UserService(
            model_schema_class=UserModel,
            postgres_service=PostgresService(session=pg_session, model_class=UserModel),
        ),
        postgres_service=PostgresService(session=pg_session, model_class=UserModel),
        redis_service=RedisCacheService(redis=redis),
        auth_jwt=auth_jwt,
    )
