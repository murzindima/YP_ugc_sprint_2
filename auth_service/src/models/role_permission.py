from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.postgres import Base


class RolePermission(Base):
    """Association table between roles and permissions."""

    __tablename__ = "role_permissions"

    role_id = Column(
        UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )
    permission_id = Column(
        UUID(as_uuid=True),
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    )

    role = relationship("Role", back_populates="permissions", passive_deletes=True)
    permission = relationship(
        "Permission", back_populates="roles", passive_deletes=True, lazy="joined"
    )

    def __repr__(self) -> str:
        """String representation of the RolePermission object."""
        return f"<RolePermission role_id={self.role_id} permission_id={self.permission_id}>"
