from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import mongo_settings


def get_mongo_client() -> AsyncIOMotorClient:
    """Get the Mongo client instance."""
    mongo_client = AsyncIOMotorClient(
        host=mongo_settings.host,
        port=mongo_settings.port,
        username=mongo_settings.user,
        password=mongo_settings.password,
        uuidRepresentation="standard",
    )
    mongo_client.db_name = mongo_settings.db
    return mongo_client
