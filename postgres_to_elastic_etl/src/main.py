from datetime import datetime
from time import sleep

from data_transformer import DataTransformer
from elasticsearch_loader import ElasticsearchLoader
from logger import logger
from postgres_extractor import PostgresExtractor
from settings import (
    TIMEOUT,
    MOVIES_STATE_KEY,
    PERSONS_STATE_KEY,
    GENRES_STATE_KEY,
    MOVIES_INDEX_NAME,
    PERSONS_INDEX_NAME,
    GENRES_INDEX_NAME,
)
from elasticsearch_mapping import (
    MOVIE_INDEX_MAPPING,
    PERSON_INDEX_MAPPING,
    GENRE_INDEX_MAPPING,
)
from state.json_file_storage import JsonFileStorage
from state.state import State

if __name__ == "__main__":
    state = State(JsonFileStorage(logger=logger))

    postgres_extractor = PostgresExtractor()
    data_transformer = DataTransformer()
    es_loader = ElasticsearchLoader()

    es_loader.create_index(MOVIES_INDEX_NAME, MOVIE_INDEX_MAPPING)
    es_loader.create_index(PERSONS_INDEX_NAME, PERSON_INDEX_MAPPING)
    es_loader.create_index(GENRES_INDEX_NAME, GENRE_INDEX_MAPPING)

    movies_saver_coro = es_loader.load_movies(state)
    movies_transformer_coro = data_transformer.transform_movies(
        next_node=movies_saver_coro
    )
    movies_fetcher_coro = postgres_extractor.fetch_updated_movies(
        movies_transformer_coro
    )
    persons_saver_coro = es_loader.load_persons(state)
    persons_transformer_coro = data_transformer.transform_persons(
        next_node=persons_saver_coro
    )
    persons_fetcher_coro = postgres_extractor.fetch_updated_persons(
        persons_transformer_coro
    )
    genres_saver_coro = es_loader.load_genres(state)
    genres_transformer_coro = data_transformer.transform_genres(
        next_node=genres_saver_coro
    )
    genres_fetcher_coro = postgres_extractor.fetch_updated_genres(
        genres_transformer_coro
    )

    while True:
        movies_fetcher_coro.send(state.get_state(MOVIES_STATE_KEY) or str(datetime.min))
        persons_fetcher_coro.send(
            state.get_state(PERSONS_STATE_KEY) or str(datetime.min)
        )
        genres_fetcher_coro.send(state.get_state(GENRES_STATE_KEY) or str(datetime.min))
        sleep(TIMEOUT)
