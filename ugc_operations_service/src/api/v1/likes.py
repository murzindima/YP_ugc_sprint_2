from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic_mongo import ObjectIdField

from src.schemas.base import BaseDelete
from src.schemas.like import Like as Like, LikeCreate
from src.services.like import LikeService, get_like_service

router = APIRouter()


@router.post("/", response_model=Like, status_code=status.HTTP_201_CREATED)
async def create_like(
    like: LikeCreate,
    like_service: LikeService = Depends(get_like_service),
) -> Like:
    """Create a new like."""
    new_like = await like_service.create_like(like)
    return new_like


@router.put("/{like_id}", response_model=Like, status_code=status.HTTP_200_OK)
async def update_like(
    like_id: ObjectIdField,
    new_like: LikeCreate,
    like_service: LikeService = Depends(get_like_service),
) -> Like:
    """Update a like by identifier."""
    updated_like = await like_service.update_model(like_id, new_like)
    return updated_like


@router.delete("/{like_id}", response_model=BaseDelete, status_code=status.HTTP_200_OK)
async def delete_like(
    like_id: ObjectIdField,
    like_service: LikeService = Depends(get_like_service),
) -> BaseDelete:
    """Delete a like by identifier."""
    deleted_like = await like_service.delete_model(like_id)
    return deleted_like


@router.get("/{movie_id}", response_model=list[Like], status_code=status.HTTP_200_OK)
async def movie_likes(
    movie_id: UUID,
    like_service: LikeService = Depends(get_like_service),
    sort: str = "date",
) -> list[Like]:
    """Returns all likes for a movie."""
    likes = await like_service.get_likes_by_movie_id(movie_id, sort)
    return likes
