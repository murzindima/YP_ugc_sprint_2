from uuid import UUID

from src.db.mongo import get_mongo_client
from src.schemas.like import Like, LikeCreate
from src.services.base import BaseService
from src.services.data_repository.mongo import MongoService


class LikeService(BaseService):
    """Service class for managing bookmarks, extending the BaseService."""

    async def create_like(self, like: LikeCreate) -> Like:
        """Create a new like."""
        _like = await self.mongo_service.get_likes_by_user_id_and_movie_id(
            like.user_id, like.movie_id
        )
        if _like:
            return _like[0]
        return await self.mongo_service.create(like)

    async def get_likes_by_movie_id(
        self, movie_id: UUID, sort: str = "date"
    ) -> list[Like]:
        """Retrieve all likes by movie identifier."""
        db_likes = await self.mongo_service.get_likes_by_movie_id(movie_id)
        return [self.model_schema_class.model_validate(like) for like in db_likes]


def get_like_service() -> LikeService:
    """Dependency function to get an instance of the LikeService."""
    client = get_mongo_client()
    return LikeService(
        model_schema_class=Like,
        mongo_service=MongoService(
            client=client, collection_name="likes", model_class=Like
        ),
    )
