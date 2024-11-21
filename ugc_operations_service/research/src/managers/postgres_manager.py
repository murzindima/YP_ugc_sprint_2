import asyncpg

INSERT_LIKES = """
    INSERT INTO likes (user_id, movie_id, score, created_at)
    VALUES ($1, $2, $3, $4);
"""
INSERT_REVIEWS = """
    INSERT INTO reviews (user_id, movie_id, text, score, created_at)
    VALUES ($1, $2, $3, $4, $5);
"""
INSERT_BOOKMARKS = """
    INSERT INTO bookmarks (user_id, movie_id, created_at)
    VALUES ($1, $2, $3);
"""


class PostgresManager:
    """Manager class for handling PostgreSQL interactions asynchronously."""

    def __init__(self, dsn):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=self.dsn)

    async def close(self):
        if self.pool:
            await self.pool.close()

    async def purge_database(self):
        async with self.pool.acquire() as connection:
            purge_queries = [
                "DROP TABLE IF EXISTS likes;",
                "DROP TABLE IF EXISTS reviews;",
                "DROP TABLE IF EXISTS bookmarks;",
            ]
            for query in purge_queries:
                await connection.execute(query)

    async def create_tables(self):
        async with self.pool.acquire() as connection:
            queries = [
                """
                CREATE TABLE IF NOT EXISTS likes (
                    id SERIAL PRIMARY KEY,
                    user_id UUID NOT NULL,
                    movie_id UUID NOT NULL,
                    score SMALLINT NOT NULL,
                    created_at TIMESTAMP NOT NULL
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS reviews (
                    id SERIAL PRIMARY KEY,
                    user_id UUID NOT NULL,
                    movie_id UUID NOT NULL,
                    text TEXT NOT NULL,
                    score SMALLINT NOT NULL,
                    created_at TIMESTAMP NOT NULL
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS bookmarks (
                    id SERIAL PRIMARY KEY,
                    user_id UUID NOT NULL,
                    movie_id UUID NOT NULL,
                    created_at TIMESTAMP NOT NULL
                );
                """,
            ]
            for query in queries:
                await connection.execute(query)

    async def insert_many(self, query: str, records: list[tuple]) -> None:
        async with self.pool.acquire() as connection:
            await connection.executemany(query, records)

    async def insert_one(self, query: str, record: tuple) -> None:
        async with self.pool.acquire() as connection:
            await connection.execute(query, *record)

    async def create_indexes(self):
        async with self.pool.acquire() as connection:
            await connection.execute(
                "CREATE INDEX idx_likes_user_id ON likes (user_id);"
            )
            await connection.execute(
                "CREATE INDEX idx_likes_user_id_score ON likes (user_id, score);"
            )
            await connection.execute(
                "CREATE INDEX idx_likes_movie_id ON likes (movie_id);"
            )

            await connection.execute(
                "CREATE INDEX idx_reviews_user_id ON reviews (user_id);"
            )
            await connection.execute(
                "CREATE INDEX idx_reviews_movie_id ON reviews (movie_id);"
            )

            await connection.execute(
                "CREATE INDEX idx_bookmarks_user_id ON bookmarks (user_id);"
            )
            await connection.execute(
                "CREATE INDEX idx_bookmarks_movie_id ON bookmarks (movie_id);"
            )
