from uuid import UUID

from src.db.mongo import get_mongo_client
from src.schemas.bookmark import Bookmark, BookmarkCreate
from src.services.base import BaseService
from src.services.data_repository.mongo import MongoService


class BookmarkService(BaseService):
    """Service class for managing bookmarks, extending the BaseService."""

    async def create_bookmark(self, bookmark: BookmarkCreate) -> Bookmark:
        """Create a new bookmark."""
        _bookmark = await self.mongo_service.get_bookmarks_by_user_id_and_movie_id(
            bookmark.user_id, bookmark.movie_id
        )
        if _bookmark:
            return _bookmark[0]
        return await self.mongo_service.create(bookmark)

    async def get_bookmarks_by_user_id(self, user_id: UUID) -> list[Bookmark]:
        """Retrieve all bookmarks by user identifier."""
        db_bookmarks = await self.mongo_service.get_bookmarks_by_user_id(user_id)
        return [
            self.model_schema_class.model_validate(bookmark)
            for bookmark in db_bookmarks
        ]


def get_bookmark_service() -> BookmarkService:
    """Dependency function to get an instance of the BookmarkService."""
    client = get_mongo_client()
    return BookmarkService(
        model_schema_class=Bookmark,
        mongo_service=MongoService(
            client=client, collection_name="bookmarks", model_class=Bookmark
        ),
    )
