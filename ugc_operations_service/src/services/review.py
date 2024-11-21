from uuid import UUID

from pydantic_mongo import ObjectIdField

from src.db.mongo import get_mongo_client
from src.schemas.review import Review, ReviewCreate
from src.services.base import BaseService
from src.services.data_repository.mongo import MongoService


class ReviewService(BaseService):
    """Service class for managing bookmarks, extending the BaseService."""

    async def create_review(self, review: ReviewCreate) -> Review:
        _review = await self.mongo_service.get_reviews_by_user_id_and_movie_id(
            review.user_id, review.movie_id
        )
        if _review:
            return _review[0]
        return await self.mongo_service.create(review)

    async def get_reviews_by_movie_id(
        self, movie_id: UUID, sort: str = "date"
    ) -> list[Review]:
        """Retrieve all reviews by movie identifier."""
        db_reviews = await self.mongo_service.get_reviews_by_movie_id(movie_id)
        return [self.model_schema_class.model_validate(review) for review in db_reviews]

    async def like_review(self, review_id: ObjectIdField) -> Review:
        """Like a review."""
        db_review = await self.mongo_service.get_by_id(review_id)
        db_review.likes += 1
        db_review_dict = db_review.model_dump(exclude={"_id"})
        update_doc = ReviewCreate(**db_review_dict)
        db_model = await self.mongo_service.update(review_id, update_doc)
        return self.model_schema_class.model_validate(db_model)

    async def dislike_review(self, review_id: ObjectIdField) -> Review:
        """Dislike a review."""
        db_review = await self.mongo_service.get_by_id(review_id)
        db_review.dislikes += 1
        db_review_dict = db_review.model_dump(exclude={"_id"})
        update_doc = ReviewCreate(**db_review_dict)
        db_model = await self.mongo_service.update(review_id, update_doc)
        return self.model_schema_class.model_validate(db_model)


def get_review_service() -> ReviewService:
    """Dependency function to get an instance of the ReviewService."""
    client = get_mongo_client()
    return ReviewService(
        model_schema_class=Review,
        mongo_service=MongoService(
            client=client, collection_name="reviews", model_class=Review
        ),
    )
