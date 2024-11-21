from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from core.messages import GENRE_NOT_FOUND, GENRES_NOT_FOUND
from queries.genre import GenreFilter
from schemas.genre import Genre as GenreSchema
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get("/", response_model=list[GenreSchema])
async def all_genres(
    genre_service: GenreService = Depends(get_genre_service),
    genre_filter: GenreFilter = Depends(),
) -> list[GenreSchema]:
    """
    Returns all genres with pagination.
    """
    genres = await genre_service.get_all_models(genre_filter)

    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRES_NOT_FOUND)

    return [GenreSchema(**genre.model_dump()) for genre in genres]


@router.get("/{genre_id}", response_model=GenreSchema)
async def genre_details(
    genre_id: str, genre_service: GenreService = Depends(get_genre_service)
) -> GenreSchema:
    """
    Returns the genre by identifier.
    """

    genre = await genre_service.get_model_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRE_NOT_FOUND)

    return GenreSchema(**genre.model_dump())
