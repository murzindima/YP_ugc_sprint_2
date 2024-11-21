import csv

import asyncpg
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from tqdm import tqdm

from helpers import logger


class CSVManager:
    """Manager class for interacting with CSV file format."""

    @staticmethod
    async def write_to_csv(file_path: str, records: list[tuple]) -> None:
        try:
            with open(file_path, "a", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerows(records)
        except Exception as e:
            logger.error(f"Error writing to CSV file: {e}")

    @staticmethod
    async def copy_csv_to_postgres_table(
        dsn: str, table_name_and_columns: str, csv_file_path: str
    ):
        try:
            connection = await asyncpg.connect(dsn)
            async with connection.transaction():
                copy_query = (
                    f"COPY {table_name_and_columns} FROM '{csv_file_path}' WITH CSV"
                )
                await connection.execute(copy_query)

        except Exception as e:
            logger.error(f"Error loading data to PostgreSQL: {e}")

        finally:
            await connection.close()  # type: ignore

    async def load_csv_to_postgres(self, dsn: str):
        tables_and_files = [
            ("likes(user_id, movie_id, score, created_at)", "likes"),
            ("reviews(user_id, movie_id, text, score, created_at)", "reviews"),
            ("bookmarks(user_id, movie_id, created_at)", "bookmarks"),
        ]
        for table, file in tqdm(tables_and_files):
            await self.copy_csv_to_postgres_table(
                dsn=dsn, table_name_and_columns=table, csv_file_path=f"/data/{file}.csv"
            )
        logger.info("PostreSQL is ready to show its performance.")

    @staticmethod
    async def copy_csv_to_mongo_collection(
        csv_file_path: str,
        collection: AsyncIOMotorCollection,
        fieldnames: list[str],
        batch_size: int = 5000,
    ):
        try:
            with open(csv_file_path, "r", encoding="utf-8") as csv_file:
                csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
                batch = []
                for row in csv_reader:
                    if "score" in row:
                        row["score"] = int(row["score"])

                    batch.append(row)

                    if len(batch) == batch_size:
                        await collection.insert_many(batch)
                        batch = []

                if batch:
                    await collection.insert_many(batch)

        except Exception as e:
            logger.error(f"Error loading data to MongoDB: {e}")

    async def load_csv_to_mongo(self, mongo_db: AsyncIOMotorDatabase):
        collections_files_fields = [
            (
                mongo_db["likes"],
                "data/likes.csv",
                ["user_id", "movie_id", "score", "created_at"],
            ),
            (
                mongo_db["reviews"],
                "data/reviews.csv",
                ["user_id", "movie_id", "text", "score", "created_at"],
            ),
            (
                mongo_db["bookmarks"],
                "data/bookmarks.csv",
                ["user_id", "movie_id", "created_at"],
            ),
        ]
        for collection, file, fieldnames in tqdm(collections_files_fields):
            await self.copy_csv_to_mongo_collection(file, collection, fieldnames)
        logger.info("MongoDB is ready to show its performance.")
