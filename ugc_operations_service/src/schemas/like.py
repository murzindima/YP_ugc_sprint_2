from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ConfigDict

from src.schemas.base import ObjectIDMixin


class LikeCreate(BaseModel):
    movie_id: UUID
    user_id: UUID
    score: int = Field(..., ge=0, le=10)

    @field_validator("score")
    def score_must_be_valid(cls, v):
        if v < 0 or v > 10:
            raise ValueError("Score must be between 0 and 10")
        return v


class Like(ObjectIDMixin, LikeCreate):
    model_config = ConfigDict(extra="allow")
    pass
