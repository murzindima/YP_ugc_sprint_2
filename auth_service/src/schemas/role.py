from uuid import UUID

from pydantic import BaseModel

from src.models.role import RoleType


class RoleCreate(BaseModel):
    """Schema for creating a new role."""

    name: RoleType
    description: str | None = None


class RoleUpdate(BaseModel):
    """Schema for updating a role."""

    name: RoleType | None = None
    description: str | None = None


class Role(BaseModel):
    """Schema for a role."""

    id: UUID
    name: RoleType
    description: str | None

    class Config:
        from_attributes = True
