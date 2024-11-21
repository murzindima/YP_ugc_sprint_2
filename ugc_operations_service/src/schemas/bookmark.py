from uuid import UUID

from pydantic import BaseModel

from src.schemas.base import ObjectIDMixin


class Bookmark(ObjectIDMixin):
    user_id: UUID
    movie_id: UUID


class BookmarkCreate(BaseModel):
    user_id: UUID
    movie_id: UUID
