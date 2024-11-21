from contextlib import asynccontextmanager

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

ASCENDING = 1


class MongoManager:
    """Manager class for handling MongoDB interactions asynchronously."""

    def __init__(self, uri, database_name):
        self.client = AsyncIOMotorClient(uri)
        self.db: AsyncIOMotorDatabase = self.client[database_name]

    @asynccontextmanager
    async def get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        collection = self.db[collection_name]
        try:
            yield collection
        finally:
            pass

    async def purge_database(self):
        collections = await self.db.list_collection_names()
        for collection_name in collections:
            await self.db.drop_collection(collection_name)

    async def create_collections(self):
        collections = ["likes", "reviews", "bookmarks"]
        for collection_name in collections:
            await self.db.create_collection(collection_name)

    async def insert_many(self, collection: str, documents: list[dict]) -> None:
        async with self.get_collection(collection) as collection:
            if documents:
                await collection.insert_many(documents)

    async def insert_one(self, collection: str, document: dict) -> None:
        async with self.get_collection(collection) as collection:
            if document:
                await collection.insert_one(document)

    async def create_indexes(self):
        async with self.get_collection("likes") as collection:
            await collection.create_index([("movie_id", ASCENDING)])

            await collection.create_index([("user_id", ASCENDING)])
            await collection.create_index(
                [("user_id", ASCENDING), ("score", ASCENDING)]
            )

        async with self.get_collection("bookmarks") as collection:
            await collection.create_index([("user_id", ASCENDING)])
