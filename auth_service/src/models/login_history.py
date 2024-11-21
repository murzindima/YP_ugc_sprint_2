import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.postgres import Base


def create_partition(target, connection, **kw) -> None:
    """Create a partition by login_histories."""
    connection.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS "login_histories_smart" 
            PARTITION OF "login_histories" FOR VALUES IN ('smart')
            """
        )
    )
    connection.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS "login_histories_mobile" 
            PARTITION OF "login_histories" FOR VALUES IN ('mobile')
            """
        )
    )
    connection.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS "login_histories_web" 
            PARTITION OF "login_histories" FOR VALUES IN ('web')
            """
        )
    )


class LoginHistory(Base):
    """Model representing a user's login history."""

    __tablename__ = "login_histories"
    __table_args__ = (
        UniqueConstraint("id", "device"),
        {
            "postgresql_partition_by": "LIST (device)",
            "listeners": [("after_create", create_partition)],
        },
    )

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
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(50))
    location = Column(String(255))
    os = Column(String(50))
    browser = Column(String(50))
    device = Column(String(50))
    refresh_token = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="login_histories", passive_deletes=True)

    def __repr__(self) -> str:
        """String representation of the LoginHistory object."""
        return f"<LoginHistory user_id={self.user_id} timestamp={self.timestamp}>"
