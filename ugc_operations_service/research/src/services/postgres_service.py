from datetime import datetime
from random import randint
from uuid import uuid4

from helpers import set_timer
from managers.csv_manager import CSVManager
from managers.postgres_manager import (
    INSERT_BOOKMARKS,
    INSERT_LIKES,
    INSERT_REVIEWS,
    PostgresManager,
)


class PostgresService:
    """Postgres service for interacting with the Postgres DB."""

    additional_records_amount = 100

    def __init__(self, dsn):
        self.pg_manager = PostgresManager(dsn=dsn)
        self.csv_manager = CSVManager()

    async def get_liked_movies_by_user(self, user_id: str) -> list[str]:
        async with self.pg_manager.pool.acquire() as connection:
            select_query = """
                    SELECT movie_id FROM likes
                    WHERE user_id = $1 AND score = 10;
                """
            rows = await connection.fetch(select_query, user_id)
            return [str(row["movie_id"]) for row in rows]

    async def get_bookmarked_movies_by_user(self, user_id: str) -> list[str]:
        async with self.pg_manager.pool.acquire() as connection:
            select_query = """SELECT movie_id FROM bookmarks WHERE user_id = $1;"""
            rows = await connection.fetch(select_query, user_id)
            return [str(row["movie_id"]) for row in rows]

    async def get_movie_likes_amount(self, movie_id: str) -> int:
        async with self.pg_manager.pool.acquire() as connection:
            select_query = """SELECT COUNT(*) FROM likes WHERE movie_id = $1;"""
            row = await connection.fetchrow(select_query, movie_id)
            return row["count"]

    async def get_movie_likes_and_dislikes_amount(self, movie_id: str) -> dict:
        async with self.pg_manager.pool.acquire() as connection:
            select_query = """
                    SELECT
                        COUNT(*) FILTER (WHERE score = 10) AS likes_count,
                        COUNT(*) FILTER (WHERE score = 0) AS dislikes_count
                    FROM likes
                    WHERE movie_id = $1;
                """
            rows = await connection.fetch(select_query, movie_id)
            return {
                "likes": rows[0]["likes_count"],
                "dislikes": rows[0]["dislikes_count"],
            }

    async def get_average_movie_score(self, movie_id: str) -> float:
        async with self.pg_manager.pool.acquire() as connection:
            select_query = """
                    SELECT AVG(score) as avg_rating
                    FROM likes
                    WHERE movie_id = $1;
                """
            row = await connection.fetchrow(select_query, movie_id)
            return row["avg_rating"] if row["avg_rating"] is not None else 0.0

    async def get_random_record_from_table(self, table: str, attribute: str) -> str:
        async with self.pg_manager.pool.acquire() as connection:
            select_query = f"""
                    SELECT {attribute} FROM {table}
                    ORDER BY RANDOM()
                    LIMIT 1;
                """
            row = await connection.fetchrow(select_query)
            return row[attribute]

    async def insert_movie_score(self, user_id: str, movie_id: str, score: int) -> None:
        await self.pg_manager.insert_one(
            query=INSERT_LIKES, record=(user_id, movie_id, score, datetime.now())
        )

    async def insert_review(
        self, user_id: str, movie_id: str, review_text: str, score: int
    ) -> None:
        await self.pg_manager.insert_one(
            query=INSERT_REVIEWS,
            record=(user_id, movie_id, review_text, score, datetime.now()),
        )

    async def insert_bookmark(self, user_id: str, movie_id: str) -> None:
        await self.pg_manager.insert_one(
            query=INSERT_BOOKMARKS, record=(user_id, movie_id, datetime.now())
        )

    @set_timer(n=additional_records_amount)
    async def add_realtime_records(
        self, users_ids: tuple[str, ...], movies_ids: tuple[str, ...]
    ) -> None:
        for user_id, movie_id in zip(users_ids, movies_ids):
            await self.insert_movie_score(user_id, movie_id, randint(0, 10))
            await self.insert_review(user_id, movie_id, "crazy movie", randint(0, 10))
            await self.insert_bookmark(user_id, movie_id)

    @set_timer(n=additional_records_amount)
    async def read_operations(
        self, users_ids: tuple[str, ...], movies_ids: tuple[str, ...]
    ) -> None:
        for user_id, movie_id in zip(users_ids, movies_ids):
            await self.get_liked_movies_by_user(user_id)
            await self.get_bookmarked_movies_by_user(user_id)
            await self.get_movie_likes_amount(user_id)
            await self.get_movie_likes_and_dislikes_amount(movie_id)
            await self.get_average_movie_score(movie_id)

    async def prepare_database(self) -> None:
        try:
            await self.pg_manager.connect()
            await self.pg_manager.purge_database()
            await self.pg_manager.create_tables()
            await self.pg_manager.create_indexes()
            await self.csv_manager.load_csv_to_postgres(dsn=self.pg_manager.dsn)

        finally:
            await self.pg_manager.close()

    async def run(self):
        try:
            await self.pg_manager.connect()

            users_ids = tuple(
                str(uuid4()) for _ in range(self.additional_records_amount)
            )
            movies_ids = tuple(
                str(uuid4()) for _ in range(self.additional_records_amount)
            )
            await self.add_realtime_records(users_ids, movies_ids)
            await self.read_operations(users_ids, movies_ids)

        finally:
            await self.pg_manager.close()
