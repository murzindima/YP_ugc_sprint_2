from typing import Generator

from decorators import coroutine
from state.models import Movie, Person, Genre, FilmRoles, PersonFilms


class DataTransformer:
    """
    A class for processing loaded data.

    This class is designed to handle the transformation of raw data into structured
    formats, suitable for further processing or storage. It typically works with data
    loaded from external sources and converts it into a more usable form.
    """

    @staticmethod
    @coroutine
    def transform_movies(
        next_node: Generator,
    ) -> Generator[list[Movie], list[dict], None]:
        """
        Coroutine for transforming movie records into Pydantic models.

        This coroutine takes a batch of movie records (as dictionaries) and transforms them
        into Pydantic `Movie` model instances. It is designed to work as part of a coroutine
        chain, receiving input from and sending output to other coroutines.

        Parameters:
        next_node (Generator): The next coroutine in the pipeline to which the transformed
                               batch of `Movie` models will be sent.

        Yields:
        list[Movie]: A list of `Movie` model instances created from the input movie records.

        Receives:
        list[dict]: A batch of movie records, where each record is a dictionary of movie data.

        Returns:
        None
        """
        while filmworks := (yield):  # type: ignore
            batch = []
            for filmwork in filmworks:
                uuid = filmwork.get("uuid")
                if uuid is None:
                    raise ValueError("UUID is missing in filmwork")
                title = filmwork.get("title")
                if title is None:
                    raise ValueError("Title is missing in filmwork")
                description = filmwork.get("description")
                if description is None:
                    raise ValueError("Description is missing in filmwork")
                modified = filmwork.get("modified")
                if modified is None:
                    raise ValueError("Modified is missing in filmwork")

                movie = Movie(
                    uuid=uuid,
                    title=title,
                    description=description,
                    rating=filmwork.get("rating"),
                    modified=modified,
                    genres=[Genre(**genre) for genre in filmwork.get("genres", [])],
                    directors=[
                        Person(**director) for director in filmwork.get("directors", [])
                    ],
                    actors=[Person(**actor) for actor in filmwork.get("actors", [])],
                    writers=[
                        Person(**writer) for writer in filmwork.get("writers", [])
                    ],
                )
                batch.append(movie)
            next_node.send(batch)

    @staticmethod
    @coroutine
    def transform_persons(
        next_node: Generator,
    ) -> Generator[list[PersonFilms], list[dict], None]:
        """
        Coroutine for transforming person records into Pydantic models.

        This coroutine takes a batch of person records (as dictionaries) and transforms them
        into Pydantic `Person` model instances. It handles the conversion of the `id` field to
        a UUID and structures the `films` field as required by the model.

        Parameters:
        - next_node (Generator): The next coroutine in the pipeline to which the transformed
                                 batch of `Person` models will be sent.

        Yields:
        - list[Person]: A list of `Person` model instances created from the input person records.

        Receives:
        - list[dict]: A batch of person records, where each record is a dictionary of person data.

        Returns:
        - None
        """

        while persons := (yield):  # type: ignore
            batch = []
            for person in persons:
                person_id = person.get("uuid")
                if person_id is None:
                    raise ValueError("UUID is missing in person")
                full_name = person.get("full_name")
                if full_name is None:
                    raise ValueError("Full name is missing in person")
                modified = person.get("modified")
                if modified is None:
                    raise ValueError("Modified is missing in person")

                # Process films
                films = []
                for film in person.get("films", []):
                    try:
                        film_id = film.get("uuid")
                        films.append(
                            FilmRoles(uuid=film_id, roles=film.get("roles", []))
                        )
                    except (ValueError, TypeError):
                        continue

                person_model = PersonFilms(
                    uuid=person_id,
                    full_name=full_name,
                    films=films,
                    modified=modified,
                )
                batch.append(person_model)
            try:
                next_node.send(batch)
            except StopIteration:
                break

    @staticmethod
    @coroutine
    def transform_genres(
        next_node: Generator,
    ) -> Generator[list[Genre], list[dict], None]:
        """
        Coroutine for transforming genre records into Pydantic models.

        This coroutine takes a batch of genre records (as dictionaries) and transforms them
        into Pydantic `Genre` model instances.
        It is designed to work as part of a coroutine
        chain, receiving input from and sending output to other coroutines.

        Parameters:
        next_node (Generator): The next coroutine in the pipeline to which the transformed
                               batch of `Genre` models will be sent.

        Yields:
        list[Genre]: A list of `Genre` model instances created from the input genre records.

        Receives:
        list[dict]: A batch of genre records, where each record is a dictionary of genre data.

        Returns:
        None
        """
        while genres := (yield):  # type: ignore
            batch = []
            for genre in genres:
                genre_id = genre.get("uuid")
                if genre_id is None:
                    raise ValueError("UUID is missing in genre")
                name = genre.get("name")
                if name is None:
                    raise ValueError("Name is missing in genre")
                modified = genre.get("modified")
                if modified is None:
                    raise ValueError("Modified is missing in genre")

                genre_model = Genre(
                    uuid=genre_id,
                    name=name,
                    modified=modified,
                )
                batch.append(genre_model)
            try:
                next_node.send(batch)
            except StopIteration:
                break
