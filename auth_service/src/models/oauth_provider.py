import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.postgres import Base


class OAuthProvider(Base):
    __tablename__ = "oauth_providers"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    provider_name = Column(String(50), nullable=False)
    provider_user_id = Column(String(255), nullable=False)

    user = relationship(
        "User", back_populates="oauth_providers", passive_deletes=True, lazy="joined"
    )

    access_token = Column(Text)
    refresh_token = Column(Text)
    token_expires_at = Column(DateTime)
    # TODO: add encrypted fields for access_token, refresh_token, and token_expires_at
    #       or store them in a Vault?

    def __repr__(self) -> str:
        """String representation of the OAuthProvider object."""
        return f"<OAuthProvider {self.provider_name} for user {self.user_id}>"
