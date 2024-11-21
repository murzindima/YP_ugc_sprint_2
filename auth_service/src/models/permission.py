import uuid
from enum import Enum, unique

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.postgres import Base


@unique
class PermissionType(Enum):
    VIEW = "VIEW"
    CREATE = "CREATE"
    EDIT = "EDIT"
    DELETE = "DELETE"


class Permission(Base):
    """Model representing a permission."""

    __tablename__ = "permissions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String(100), unique=True, nullable=False)

    roles = relationship(
        "RolePermission", back_populates="permission", passive_deletes=True
    )

    def __repr__(self) -> str:
        """String representation of the Permission object."""
        return f"<Permission {self.name}>"
