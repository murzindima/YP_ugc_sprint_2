from uuid import UUID

from pydantic import BaseModel


class PermissionCreate(BaseModel):
    """Schema for creating a new permission."""

    name: str


class PermissionUpdate(BaseModel):
    """Schema for updating a permission."""

    name: str | None = None


class Permission(BaseModel):
    """Schema for a permission."""

    id: UUID
    name: str

    class Config:
        from_attributes = True
