from datetime import datetime
from random import randint
from uuid import uuid4

from helpers import set_timer
from managers.csv_manager import CSVManager
from managers.data_manager import DataManager
from managers.mongo_manager import MongoManager


class MongoService:
    """Mongo service for interacting with the mongoDB."""

    additional_records_amount = 100

    def __init__(self, uri, database_name):
        self.mongo_manager = MongoManager(uri=uri, database_name=database_name)
        self.data_generator = DataManager()
        self.csv_manager = CSVManager()

    async def get_liked_movies_by_user(self, user_id: str) -> list[str]:
        async with self.mongo_manager.get_collection("likes") as collection:
            cursor = collection.find({"user_id": user_id, "score": 10})
            return [document["movie_id"] async for document in cursor]

    async def get_bookmarked_movies_by_user(self, user_id: str) -> list[str]:
        async with self.mongo_manager.get_collection("bookmarks") as collection:
            cursor = collection.find({"user_id": user_id})
            return [document["movie_id"] async for document in cursor]

    async def get_movie_likes_amount(self, movie_id: str) -> int:
        async with self.mongo_manager.get_collection("likes") as collection:
            return await collection.count_documents({"movie_id": movie_id})

    async def get_movie_likes_and_dislikes_amount(self, movie_id: str) -> dict:
        async with self.mongo_manager.get_collection("likes") as collection:
            pipeline = [
                {"$match": {"movie_id": movie_id}},
                {
                    "$group": {
                        "_id": None,
                        "likes_count": {
                            "$sum": {"$cond": [{"$eq": ["$score", 10]}, 1, 0]}
                        },
                        "dislikes_count": {
                            "$sum": {"$cond": [{"$eq": ["$score", 0]}, 1, 0]}
                        },
                    }
                },
            ]
            result = await collection.aggregate(pipeline).to_list(length=None)
            return {
                "likes": result[0]["likes_count"] if result else 0,
                "dislikes": result[0]["dislikes_count"] if result else 0,
            }

    async def get_average_movie_score(self, movie_id: str) -> float:
        async with self.mongo_manager.get_collection("likes") as collection:
            pipeline = [
                {"$match": {"movie_id": movie_id}},
                {"$group": {"_id": None, "avg_rating": {"$avg": "$score"}}},
            ]
            result = await collection.aggregate(pipeline).to_list(length=None)
            return result[0]["avg_rating"] if result else 0.0

    async def insert_movie_score(self, user_id: str, movie_id: str, score: int) -> None:
        await self.mongo_manager.insert_one(
            collection="likes",
            document={
                "user_id": user_id,
                "movie_id": movie_id,
                "score": score,
                "created_at": datetime.now(),
            },
        )

    async def insert_review(
        self, user_id: str, movie_id: str, text: str, score: int
    ) -> None:
        await self.mongo_manager.insert_one(
            collection="reviews",
            document={
                "user_id": user_id,
                "movie_id": movie_id,
                "text": text,
                "score": score,
                "created_at": datetime.now(),
            },
        )

    async def insert_bookmark(self, user_id: str, movie_id: str) -> None:
        await self.mongo_manager.insert_one(
            collection="bookmarks",
            document={
                "user_id": user_id,
                "movie_id": movie_id,
                "created_at": datetime.now(),
            },
        )

    async def get_random_record_from_collection(self, collection: str, attribute: str):
        async with self.mongo_manager.get_collection(collection) as collection:
            cursor = collection.aggregate([{"$sample": {"size": 1}}])
            document = await cursor.to_list(length=None)
            return document[0][attribute]

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

    async def prepare_database(self):
        await self.mongo_manager.purge_database()
        await self.mongo_manager.create_collections()
        await self.mongo_manager.create_indexes()
        await self.csv_manager.load_csv_to_mongo(self.mongo_manager.db)

    async def run(self):
        users_ids = tuple(str(uuid4()) for _ in range(self.additional_records_amount))
        movies_ids = tuple(str(uuid4()) for _ in range(self.additional_records_amount))
        await self.add_realtime_records(users_ids, movies_ids)
        await self.read_operations(users_ids, movies_ids)
