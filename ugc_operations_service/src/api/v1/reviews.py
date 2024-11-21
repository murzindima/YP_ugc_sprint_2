from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic_mongo import ObjectIdField

from src.schemas.base import BaseDelete
from src.schemas.review import Review, ReviewCreate
from src.services.review import ReviewService, get_review_service

router = APIRouter()


@router.post("/", response_model=Review, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ReviewCreate,
    review_service: ReviewService = Depends(get_review_service),
) -> Review:
    """Create a new review."""
    new_review = await review_service.create_review(review)
    return new_review


@router.get("/{movie_id}", response_model=list[Review], status_code=status.HTTP_200_OK)
async def movie_reviews(
    movie_id: UUID,
    review_service: ReviewService = Depends(get_review_service),
    sort: str = "date",
) -> list[Review]:
    """Returns all reviews for a movie."""
    reviews = await review_service.get_reviews_by_movie_id(movie_id, sort)
    return reviews


@router.post(
    "/{review_id}/like", response_model=Review, status_code=status.HTTP_201_CREATED
)
async def like_review(
    review_id: ObjectIdField,
    review_service: ReviewService = Depends(get_review_service),
) -> Review:
    """Add a like to a review."""

    liked_review = await review_service.like_review(review_id)
    return liked_review


@router.post(
    "/{review_id}/dislike", response_model=Review, status_code=status.HTTP_201_CREATED
)
async def dislike_review(
    review_id: ObjectIdField,
    review_service: ReviewService = Depends(get_review_service),
) -> Review:
    """Add a dislike to a review."""
    disliked_review = await review_service.dislike_review(review_id)
    return disliked_review


@router.delete(
    "/{review_id}", response_model=BaseDelete, status_code=status.HTTP_200_OK
)
async def delete_review(
    review_id: ObjectIdField,
    review_service: ReviewService = Depends(get_review_service),
) -> BaseDelete:
    """Delete a review by identifier."""
    deleted_review = await review_service.delete_model(review_id)
    return deleted_review
