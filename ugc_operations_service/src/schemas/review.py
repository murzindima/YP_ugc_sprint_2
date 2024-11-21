from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from src.schemas.base import ObjectIDMixin


class ReviewCreate(BaseModel):
    movie_id: UUID
    user_id: UUID
    text: str
    date_published: datetime = Field(default_factory=datetime.utcnow)
    likes: int = 0
    dislikes: int = 0
    movie_score: int | None = Field(None, ge=0, le=10)


class Review(ObjectIDMixin, ReviewCreate):
    model_config = ConfigDict(extra="allow")
    pass
