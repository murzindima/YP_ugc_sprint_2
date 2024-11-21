from datetime import datetime
from uuid import UUID

from pydantic_mongo import ObjectIdField

from src.schemas.bookmark import Bookmark
from src.schemas.like import Like
from src.schemas.review import Review
from src.services.data_repository.mongo_crud import MongoDBCrudService


class MongoService(MongoDBCrudService):
    """MongoDB service for all models."""

    async def add_like(self, like: Like) -> Like:
        return await self.create(like)

    async def get_all_likes(self) -> list[Like]:
        return await self.get_all()

    async def get_like_by_id(self, like_id: ObjectIdField):
        return await self.get_by_id(like_id)

    async def update_like(self, like_id: ObjectIdField, like: Like):
        return await self.update(like_id, like)

    async def delete_like(self, like_id: ObjectIdField):
        return await self.delete(like_id)

    async def get_likes_by_user_id(self, user_id: UUID):
        return await self.collection.find({"user_id": user_id}).to_list(None)

    async def get_likes_by_movie_id(self, movie_id: UUID):
        return await self.collection.find({"movie_id": movie_id}).to_list(None)

    async def get_likes_by_user_id_and_movie_id(self, user_id: UUID, movie_id: UUID):
        return await self.collection.find(
            {"user_id": user_id, "movie_id": movie_id}
        ).to_list(None)

    async def get_likes_by_score(self, score: int):
        return await self.collection.find({"score": score}).to_list(None)

    async def get_likes_by_user_id_and_score(self, user_id: UUID, score: int):
        return await self.collection.find({"user_id": user_id, "score": score}).to_list(
            None
        )

    async def get_likes_by_movie_id_and_score(self, movie_id: UUID, score: int):
        return await self.collection.find(
            {"movie_id": movie_id, "score": score}
        ).to_list(None)

    async def get_likes_by_user_id_and_movie_id_and_score(
        self, user_id: UUID, movie_id: UUID, score: int
    ):
        return await self.collection.find(
            {"user_id": user_id, "movie_id": movie_id, "score": score}
        ).to_list(None)

    async def add_review(self, review: Review):
        await self.create(review)

    async def get_all_reviews(self):
        return await self.get_all()

    async def get_review_by_id(self, review_id: ObjectIdField):
        return await self.get_by_id(review_id)

    async def update_review(self, review_id: ObjectIdField, review: Review):
        return await self.update(review_id, review)

    async def delete_review(self, review_id: ObjectIdField):
        return await self.delete(review_id)

    async def get_reviews_by_user_id(self, user_id: UUID):
        return await self.collection.find({"user_id": user_id}).to_list(None)

    async def get_reviews_by_movie_id(self, movie_id: UUID):
        return await self.collection.find({"movie_id": movie_id}).to_list(None)

    async def get_reviews_by_user_id_and_movie_id(self, user_id: UUID, movie_id: UUID):
        return await self.collection.find(
            {"user_id": user_id, "movie_id": movie_id}
        ).to_list(None)

    async def get_reviews_by_date_published(self, date_published: datetime):
        return await self.collection.find({"date_published": date_published}).to_list(
            None
        )

    async def get_reviews_by_user_id_and_date_published(
        self, user_id: UUID, date_published: datetime
    ):
        return await self.collection.find(
            {"user_id": user_id, "date_published": date_published}
        ).to_list(None)

    async def get_reviews_by_movie_id_and_date_published(
        self, movie_id: UUID, date_published: datetime
    ):
        return await self.collection.find(
            {"movie_id": movie_id, "date_published": date_published}
        ).to_list(None)

    async def get_reviews_by_user_id_and_movie_id_and_date_published(
        self, user_id: UUID, movie_id: UUID, date_published: datetime
    ):
        return await self.collection.find(
            {"user_id": user_id, "movie_id": movie_id, "date_published": date_published}
        ).to_list(None)

    async def get_reviews_by_likes(self, likes: int):
        return await self.collection.find({"likes": likes}).to_list(None)

    async def get_reviews_by_user_id_and_likes(self, user_id: UUID, likes: int):
        return await self.collection.find({"user_id": user_id, "likes": likes}).to_list(
            None
        )

    async def get_reviews_by_movie_id_and_likes(self, movie_id: UUID, likes: int):
        return await self.collection.find(
            {"movie_id": movie_id, "likes": likes}
        ).to_list(None)

    async def get_reviews_by_user_id_and_movie_id_and_likes(
        self, user_id: UUID, movie_id: UUID, likes: int
    ):
        return await self.collection.find(
            {"user_id": user_id, "movie_id": movie_id, "likes": likes}
        ).to_list(None)

    async def get_reviews_by_dislikes(self, dislikes: int):
        return await self.collection.find({"dislikes": dislikes}).to_list(None)

    async def get_reviews_by_user_id_and_dislikes(self, user_id: UUID, dislikes: int):
        return await self.collection.find(
            {"user_id": user_id, "dislikes": dislikes}
        ).to_list(None)

    async def get_reviews_by_movie_id_and_dislikes(self, movie_id: UUID, dislikes: str):
        return await self.collection.find(
            {"movie_id": movie_id, "dislikes": dislikes}
        ).to_list(None)

    async def get_reviews_by_user_id_and_movie_id_and_dislikes(
        self, user_id: UUID, movie_id: UUID, dislikes: int
    ):
        return await self.collection.find(
            {"user_id": user_id, "movie_id": movie_id, "dislikes": dislikes}
        ).to_list(None)

    async def get_reviews_by_movie_score(self, movie_score: int):
        return await self.collection.find({"movie_score": movie_score}).to_list(None)

    async def get_reviews_by_user_id_and_movie_score(
        self, user_id: UUID, movie_score: int
    ):
        return await self.collection.find(
            {"user_id": user_id, "movie_score": movie_score}
        ).to_list(None)

    async def get_reviews_by_movie_id_and_movie_score(
        self, movie_id: UUID, movie_score: int
    ):
        return await self.collection.find(
            {"movie_id": movie_id, "movie_score": movie_score}
        ).to_list(None)

    async def get_reviews_by_user_id_and_movie_id_and_movie_score(
        self, user_id: UUID, movie_id: UUID, movie_score: int
    ):
        return await self.collection.find(
            {"user_id": user_id, "movie_id": movie_id, "movie_score": movie_score}
        ).to_list(None)

    async def get_reviews_by_user_id_and_movie_id_and_movie_score_and_date_published(
        self, user_id: UUID, movie_id: UUID, movie_score: int, date_published: datetime
    ):
        return await self.collection.find(
            {
                "user_id": user_id,
                "movie_id": movie_id,
                "movie_score": movie_score,
                "date_published": date_published,
            }
        ).to_list(None)

    async def get_reviews_by_user_id_and_movie_id_and_movie_score_and_likes(
        self, user_id: UUID, movie_id: UUID, movie_score: int, likes: int
    ):
        return await self.collection.find(
            {
                "user_id": user_id,
                "movie_id": movie_id,
                "movie_score": movie_score,
                "likes": likes,
            }
        ).to_list(None)

    async def get_reviews_by_user_id_and_movie_id_and_movie_score_and_dislikes(
        self, user_id: UUID, movie_id: UUID, movie_score: int, dislikes: int
    ):
        return await self.collection.find(
            {
                "user_id": user_id,
                "movie_id": movie_id,
                "movie_score": movie_score,
                "dislikes": dislikes,
            }
        ).to_list(None)

    async def get_reviews_by_user_id_and_movie_id_and_movie_score_and_likes_and_dislikes(
        self, user_id: UUID, movie_id: UUID, movie_score: int, likes: int, dislikes: int
    ):
        return await self.collection.find(
            {
                "user_id": user_id,
                "movie_id": movie_id,
                "movie_score": movie_score,
                "likes": likes,
                "dislikes": dislikes,
            }
        ).to_list(None)

    async def get_reviews_by_user_id_and_movie_id_and_movie_score_and_date_published_and_likes_and_dislikes(
        self,
        user_id: UUID,
        movie_id: UUID,
        movie_score: int,
        date_published: datetime,
        likes: int,
        dislikes: int,
    ):
        return await self.collection.find(
            {
                "user_id": user_id,
                "movie_id": movie_id,
                "movie_score": movie_score,
                "date_published": date_published,
                "likes": likes,
                "dislikes": dislikes,
            }
        ).to_list(None)

    async def get_reviews_by_user_id_and_movie_id_and_movie_score_and_date_published_and_likes(
        self,
        user_id: UUID,
        movie_id: UUID,
        movie_score: int,
        date_published: datetime,
        likes: int,
    ):
        return await self.collection.find(
            {
                "user_id": user_id,
                "movie_id": movie_id,
                "movie_score": movie_score,
                "date_published": date_published,
                "likes": likes,
            }
        ).to_list(None)

    async def get_reviews_by_user_id_and_movie_id_and_movie_score_and_date_published_and_dislikes(
        self,
        user_id: UUID,
        movie_id: UUID,
        movie_score: int,
        date_published: datetime,
        dislikes: int,
    ):
        return await self.collection.find(
            {
                "user_id": user_id,
                "movie_id": movie_id,
                "movie_score": movie_score,
                "date_published": date_published,
                "dislikes": dislikes,
            }
        ).to_list(None)

    async def add_bookmark(self, bookmark: Bookmark) -> Bookmark:
        return await self.create(bookmark)

    async def get_all_bookmarks(self) -> list[Bookmark]:
        return await self.get_all()

    async def get_bookmark_by_id(self, bookmark_id: ObjectIdField):
        return await self.get_by_id(bookmark_id)

    async def update_bookmark(self, bookmark_id: ObjectIdField, bookmark: Bookmark):
        return await self.update(bookmark_id, bookmark)

    async def delete_bookmark(self, bookmark_id: ObjectIdField):
        return await self.delete(bookmark_id)

    async def get_bookmarks_by_user_id(self, user_id: UUID):
        return await self.collection.find({"user_id": user_id}).to_list(None)

    async def get_bookmarks_by_movie_id(self, movie_id: UUID):
        return await self.collection.find({"movie_id": movie_id}).to_list(None)

    async def get_bookmarks_by_user_id_and_movie_id(
        self, user_id: UUID, movie_id: UUID
    ):
        return await self.collection.find(
            {"user_id": user_id, "movie_id": movie_id}
        ).to_list(None)
