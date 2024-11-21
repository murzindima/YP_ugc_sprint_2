from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class OAuthProviderCreate(BaseModel):
    provider_name: str
    provider_user_id: str
    user_id: UUID
    access_token: str
    refresh_token: str
    token_expires_at: datetime


class OAuthProvider(BaseModel):
    provider_name: str
    provider_user_id: str
    access_token: str
    refresh_token: str
    expires_in: int
