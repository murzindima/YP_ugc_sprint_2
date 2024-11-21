import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash

from src.db.postgres import Base
from src.models.login_history import LoginHistory
from src.models.oauth_provider import OAuthProvider


class User(Base):
    """Model representing a user."""

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    role_id = Column(
        UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False
    )
    is_deleted = Column(Boolean, default=False)

    role = relationship(
        "Role", back_populates="users", passive_deletes=True, lazy="joined"
    )
    login_histories = relationship(
        "LoginHistory", back_populates="user", passive_deletes=True
    )
    oauth_providers = relationship(
        "OAuthProvider", back_populates="user", passive_deletes=True
    )

    def __init__(
        self,
        email: str,
        first_name: str,
        last_name: str,
        role_id: UUID,
        password: str | None = None,
    ) -> None:
        """Constructor for creating a new User instance."""
        self.email = email
        self.password = generate_password_hash(password) if password else None
        self.first_name = first_name
        self.last_name = last_name
        self.role_id = role_id

    def __repr__(self) -> str:
        """String representation of the User object."""
        return f"<User {self.email}>"
