import enum
import uuid
from enum import unique

from sqlalchemy import Column, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.postgres import Base
from src.models.role_permission import RolePermission


@unique
class RoleType(enum.Enum):
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    MEMBER = "MEMBER"
    SUBSCRIBER = "SUBSCRIBER"


class Role(Base):
    """Model representing a role."""

    __tablename__ = "roles"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(Enum(RoleType), nullable=False, unique=True)
    description = Column(String(500))

    permissions = relationship(
        "RolePermission", back_populates="role", lazy="joined", passive_deletes=True
    )
    users = relationship("User", back_populates="role", passive_deletes=True)

    def __repr__(self) -> str:
        """String representation of the Role object."""
        return f"<Role {self.name}>"
