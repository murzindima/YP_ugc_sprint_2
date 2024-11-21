from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from core.messages import PERSON_FILMS_NOT_FOUND, PERSON_NOT_FOUND, PERSONS_NOT_FOUND
from queries.base import BaseFilter
from queries.person import PersonFilter, SearchPersonFilter
from schemas.film import FilmBrief as FilmBriefSchema
from schemas.person import PersonFilms as PersonSchema
from services.film import FilmService, get_film_service
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get("/", response_model=list[PersonSchema])
async def all_persons(
    person_service: PersonService = Depends(get_person_service),
    person_filter: PersonFilter = Depends(),
) -> list[PersonSchema]:
    """Returns all persons with pagination."""
    persons = await person_service.get_all_models(person_filter)

    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSONS_NOT_FOUND)

    return [PersonSchema(**person.model_dump()) for person in persons]


@router.get("/search", response_model=list[PersonSchema])
async def search_persons(
    person_service: PersonService = Depends(get_person_service),
    person_filter: SearchPersonFilter = Depends(),
) -> list[PersonSchema]:
    """Returns all persons found by fuzzy search with pagination."""
    persons = await person_service.get_all_models(person_filter)

    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSONS_NOT_FOUND)

    return [PersonSchema(**person.model_dump()) for person in persons]


@router.get("/{person_id}", response_model=PersonSchema)
async def person_details(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> PersonSchema:
    """Returns the person by identifier."""
    person = await person_service.get_model_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND)

    return PersonSchema(**person.model_dump())


@router.get("/{person_id}/film", response_model=list[FilmBriefSchema])
async def person_films(
    person_id: str,
    film_service: FilmService = Depends(get_film_service),
    base_filter: BaseFilter = Depends(),
) -> list[FilmBriefSchema]:
    """Returns a list of films associated with a specific person."""
    films = await film_service.get_person_films(
        base_filter=base_filter, person_id=person_id
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=PERSON_FILMS_NOT_FOUND
        )

    return [FilmBriefSchema(**film.model_dump()) for film in films]
