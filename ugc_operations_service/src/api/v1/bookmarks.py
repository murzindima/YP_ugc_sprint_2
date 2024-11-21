from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic_mongo import ObjectIdField

from src.schemas.base import BaseDelete
from src.schemas.bookmark import Bookmark
from src.schemas.bookmark import BookmarkCreate
from src.services.bookmark import BookmarkService, get_bookmark_service

router = APIRouter()


@router.post("/", response_model=Bookmark, status_code=status.HTTP_201_CREATED)
async def create_bookmark(
    bookmark: BookmarkCreate,
    bookmark_service: BookmarkService = Depends(get_bookmark_service),
) -> Bookmark:
    """Create a new bookmark."""
    new_bookmark = await bookmark_service.create_bookmark(bookmark)
    return new_bookmark


@router.get("/{user_id}", response_model=list[Bookmark], status_code=status.HTTP_200_OK)
async def user_bookmarks(
    user_id: UUID,
    bookmark_service: BookmarkService = Depends(get_bookmark_service),
) -> list[Bookmark]:
    """Returns all user's bookmarks."""
    bookmarks = await bookmark_service.get_bookmarks_by_user_id(user_id)
    return bookmarks


@router.delete(
    "/{bookmark_id}", response_model=BaseDelete, status_code=status.HTTP_200_OK
)
async def delete_bookmark(
    bookmark_id: ObjectIdField,
    bookmark_service: BookmarkService = Depends(get_bookmark_service),
) -> BaseDelete:
    """Delete a bookmark by identifier."""
    deleted_bookmark = await bookmark_service.delete_model(bookmark_id)
    return deleted_bookmark
