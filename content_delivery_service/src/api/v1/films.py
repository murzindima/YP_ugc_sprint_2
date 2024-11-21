from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from core.messages import FILM_NOT_FOUND, FILMS_NOT_FOUND
from queries.film import FilmFilter, SearchFilmFilter
from schemas.film import Film as FilmSchema
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get("/", response_model=list[FilmSchema])
async def all_films(
    film_service: FilmService = Depends(get_film_service),
    film_filter: FilmFilter = Depends(),
) -> list[FilmSchema]:
    """Returns all films with pagination."""
    films = await film_service.get_all_models(film_filter)

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILMS_NOT_FOUND)

    return [FilmSchema(**film.model_dump()) for film in films]


@router.get("/search", response_model=list[FilmSchema])
async def search_films(
    film_service: FilmService = Depends(get_film_service),
    film_filter: SearchFilmFilter = Depends(),
) -> list[FilmSchema]:
    """Returns all films found by fuzzy search with pagination."""
    films = await film_service.get_all_models(film_filter)

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILMS_NOT_FOUND)

    return [FilmSchema(**film.model_dump()) for film in films]


@router.get("/{film_id}", response_model=FilmSchema)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> FilmSchema:
    """Returns the film by identifier."""
    film = await film_service.get_model_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)

    return FilmSchema(**film.model_dump())
