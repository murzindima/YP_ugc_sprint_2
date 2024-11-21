from typing import Generator

import backoff
from decorators import backoff_handler, coroutine, giveup_handler, success_handler
from logger import logger
from psycopg import OperationalError, ServerCursor, connect
from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row
from settings import postgres_settings
from sql_queries import GET_MOVIES_SQL, GET_PERSONS_SQL, GET_GENRES_SQL


class PostgresExtractor:
    """
    A class for extracting data from a PostgreSQL database.

    This class is designed to connect to a PostgreSQL database and retrieve data,
    specifically updated movie records. It uses a coroutine for asynchronous data
    fetching and employs a backoff strategy for handling database connection errors.
    """

    max_tries = 8

    def __init__(self):
        """
        Initializes the connection parameters and batch size for data extraction.

        Sets up the database connection string (DSN) using settings from 'postgres_settings'.
        Also, initializes the batch size for fetching records, which determines how many
        records are retrieved in each database query.
        """
        self.dsn = make_conninfo(**postgres_settings.dict())
        self.batch_size = 100

    @backoff.on_exception(
        backoff.expo,
        OperationalError,
        max_tries=max_tries,
        on_backoff=backoff_handler,
        on_success=success_handler,
        on_giveup=giveup_handler,
    )
    @coroutine
    def fetch_updated_movies(
        self, next_node: Generator
    ) -> Generator[list[dict], str, None]:
        """
        Coroutine for extracting updated movie records from the database.

        This method fetches batches of updated movie records based on a given timestamp.
        It uses a coroutine pattern for asynchronous operation, yielding batches of records
        to the next processing node in the data pipeline.

        Parameters:
        next_node (Generator): The next coroutine in the pipeline to which the extracted
                               movie records are sent.

        Yields:
        list[dict]: A batch of updated movie records in dictionary format.

        Receives:
        str: A timestamp string indicating the starting point for fetching updated records.
        """
        with (
            connect(self.dsn, row_factory=dict_row) as connection,
            ServerCursor(connection, "fetcher_movies") as cursor,
        ):
            while last_updated := (yield):  # type: ignore
                logger.info(f"Fetching movies updated after {last_updated}")
                cursor.execute(GET_MOVIES_SQL, (last_updated,))
                while movies := cursor.fetchmany(size=self.batch_size):
                    next_node.send(movies)

    @coroutine
    def fetch_updated_persons(
        self, next_node: Generator
    ) -> Generator[list[dict], str, None]:
        """
        Coroutine for extracting updated person records from the database.

        This method fetches batches of updated person records based on a given timestamp.
        It uses a coroutine pattern for asynchronous operation, yielding batches of records
        to the next processing node in the data pipeline.

        Parameters:
        next_node (Generator): The next coroutine in the pipeline to which the extracted
                               person records are sent.

        Yields:
        list[dict]: A batch of updated person records in dictionary format.

        Receives:
        str: A timestamp string indicating the starting point for fetching updated records.
        """
        with (
            connect(self.dsn, row_factory=dict_row) as connection,
            ServerCursor(connection, "fetcher_persons") as cursor,
        ):
            while last_updated := (yield):  # type: ignore
                logger.info(f"Fetching persons updated after {last_updated}")
                cursor.execute(GET_PERSONS_SQL, (last_updated,))
                while persons := cursor.fetchmany(size=self.batch_size):
                    try:
                        next_node.send(persons)
                    except StopIteration:
                        break

    @coroutine
    def fetch_updated_genres(
        self, next_node: Generator
    ) -> Generator[list[dict], str, None]:
        """
        Coroutine for extracting updated genre records from the database.

        This method fetches batches of updated genre records based on a given timestamp.
        It uses a coroutine pattern for asynchronous operation, yielding batches of records
        to the next processing node in the data pipeline.

        Parameters:
        next_node (Generator): The next coroutine in the pipeline to which the extracted
                               genre records are sent.

        Yields:
        list[dict]: A batch of updated genre records in dictionary format.

        Receives:
        str: A timestamp string indicating the starting point for fetching updated records.
        """
        with (
            connect(self.dsn, row_factory=dict_row) as connection,
            ServerCursor(connection, "fetcher_genres") as cursor,
        ):
            while last_updated := (yield):  # type: ignore
                logger.info(f"Fetching genres updated after {last_updated}")
                cursor.execute(GET_GENRES_SQL, (last_updated,))
                while genres := cursor.fetchmany(size=self.batch_size):
                    try:
                        next_node.send(genres)
                    except StopIteration:
                        break
