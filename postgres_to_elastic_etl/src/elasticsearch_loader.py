from contextlib import closing
from typing import Generator

import backoff
from decorators import backoff_handler, coroutine, giveup_handler, success_handler
from elasticsearch import Elasticsearch
from elasticsearch.helpers import BulkIndexError, bulk
from logger import logger
from settings import (
    elasticsearch_settings,
    MOVIES_INDEX_NAME,
    MOVIES_STATE_KEY,
    PERSONS_INDEX_NAME,
    PERSONS_STATE_KEY,
    GENRES_INDEX_NAME,
    GENRES_STATE_KEY,
)
from state.models import Movie, Genre, PersonFilms
from state.state import State


class ElasticsearchLoader:
    """
    A class for loading data into an Elasticsearch index.

    This class handles the operations required to create an Elasticsearch index
    and load data into it. It is designed to work with Pydantic models, specifically
    for handling movie data. The class uses a backoff strategy for error handling
    during these operations.
    """

    max_tries = 8
    hosts = [dict(elasticsearch_settings)]

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=max_tries,
        on_backoff=backoff_handler,
        on_success=success_handler,
        on_giveup=giveup_handler,
    )
    def create_index(self, index_name: str, index_mapping: dict):
        """
        Creates an Elasticsearch index with the given name and mapping.

        Parameters:
        index_name (str): The name of the index to create.
        index_mapping (dict): The mapping definition for the index.
        es_hosts (list): List of Elasticsearch host URLs.
        """
        with closing(Elasticsearch(self.hosts)) as es:
            if not es.indices.exists(index=index_name):
                es.indices.create(index=index_name, body=index_mapping)  # type: ignore
                logger.info(f'Index "{index_name}" created')
            else:
                logger.info(f'Index "{index_name}" already exists')

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=max_tries,
        on_backoff=backoff_handler,
        on_success=success_handler,
        on_giveup=giveup_handler,
    )
    @coroutine
    def load_movies(self, state: State) -> Generator[None, list[Movie], None]:
        """
        Loads Pydantic model instances into the Elasticsearch index.

        This coroutine receives batches of `Movie` model instances and indexes them into
        Elasticsearch. It handles exceptions during the data loading process using an
        exponential backoff strategy. It also logs the progress and errors encountered during
        the process.

        Parameters:
        state (State): The state object for keeping track of the data loading process.
        """
        while movies := (yield):
            logger.info(f"Received for saving {len(movies)} movies")
            with closing(Elasticsearch(self.hosts)) as es:
                actions = []
                for movie in movies:
                    action = {
                        "_index": MOVIES_INDEX_NAME,
                        "_id": movie.uuid,
                        "_source": {
                            "uuid": movie.uuid,
                            "title": movie.title,
                            "description": movie.description,
                            "imdb_rating": movie.rating,
                            "genres": [
                                genre.dict(exclude={"modified"})
                                for genre in movie.genres
                            ],
                            "actors": [actor.dict() for actor in movie.actors],
                            "directors": [
                                director.dict() for director in movie.directors
                            ],
                            "writers": [writer.dict() for writer in movie.writers],
                        },
                    }
                    actions.append(action)
                try:
                    success, _ = bulk(es, actions)
                except BulkIndexError as bulk_index:
                    logger.error("Failed to index documents:")
                    for error in bulk_index.errors:
                        logger.error(error)
                else:
                    logger.info(f"Successfully indexed {success} movies")
                    state.set_state(MOVIES_STATE_KEY, str(movies[-1].modified))

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=max_tries,
        on_backoff=backoff_handler,
        on_success=success_handler,
        on_giveup=giveup_handler,
    )
    @coroutine
    def load_persons(self, state: State) -> Generator[None, list[PersonFilms], None]:
        """
        Loads person model instances into the Elasticsearch index.

        This coroutine receives batches of `Person` model instances and indexes them into
        Elasticsearch. It handles exceptions using an exponential backoff strategy.
        """
        while persons := (yield):
            logger.info(f"Received for saving {len(persons)} persons")
            with closing(Elasticsearch(self.hosts)) as es:
                actions = [
                    {
                        "_index": PERSONS_INDEX_NAME,
                        "_id": person.uuid,
                        "_source": person.dict(exclude={"modified"}),
                    }
                    for person in persons
                ]
                try:
                    success, _ = bulk(es, actions)
                except BulkIndexError as bulk_index:
                    logger.error("Failed to index persons:")
                    for error in bulk_index.errors:
                        logger.error(error)
                else:
                    logger.info(f"Successfully indexed {success} persons")
                    state.set_state(PERSONS_STATE_KEY, str(persons[-1].modified))

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=max_tries,
        on_backoff=backoff_handler,
        on_success=success_handler,
        on_giveup=giveup_handler,
    )
    @coroutine
    def load_genres(self, state: State) -> Generator[None, list[Genre], None]:
        """
        Loads genre model instances into the Elasticsearch index.

        This coroutine receives batches of `Genre` model instances and indexes them into
        Elasticsearch. It handles exceptions using an exponential backoff strategy.
        """
        while genres := (yield):
            logger.info(f"Received for saving {len(genres)} genres")
            with closing(Elasticsearch(self.hosts)) as es:
                actions = [
                    {
                        "_index": GENRES_INDEX_NAME,
                        "_id": genre.uuid,
                        "_source": genre.dict(exclude={"modified"}),
                    }
                    for genre in genres
                ]
                try:
                    success, _ = bulk(es, actions)
                except BulkIndexError as bulk_index:
                    logger.error("Failed to index genres:")
                    for error in bulk_index.errors:
                        logger.error(error)
                else:
                    logger.info(f"Successfully indexed {success} genres")
                    state.set_state(GENRES_STATE_KEY, str(genres[-1].modified))
