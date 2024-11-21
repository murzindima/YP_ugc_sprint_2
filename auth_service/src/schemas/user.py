from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    email: EmailStr
    password: str | None = None
    first_name: str
    last_name: str
    role_id: UUID


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    email: EmailStr | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    role_id: UUID | None = None


class User(BaseModel):
    """Schema for a user."""

    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    role_id: UUID
    is_deleted: bool

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for a user login."""

    email: EmailStr
    password: str
