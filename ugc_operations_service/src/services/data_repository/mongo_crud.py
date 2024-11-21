from typing import Type, List, Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic import BaseModel
from pydantic_mongo import ObjectIdField

from src.schemas.base import BaseDelete
from src.core.config import mongo_settings
from src.services.abstract.data_storage import DataStorageService


class MongoDBCrudService[M](DataStorageService):
    """
    A base class for CRUD operations on models stored in a MongoDB database.

    This class offers a generic implementation for creating, reading, updating, and deleting (CRUD) documents
    in a specified MongoDB collection. It utilizes Pydantic models for data validation and serialization,
    facilitating the handling of BSON format data.

    Attributes:
        db (AsyncIOMotorClient[db_name]): The database instance for CRUD operations.
        collection (Collection): The MongoDB collection that the service interacts with.
        model_class (Type[M]): The Pydantic model class used for data validation.

    Methods:
        get_all: Retrieves a list of all documents in the collection.
        get_by_id: Retrieves a document by its unique ObjectId.
        create: Creates a new document in the collection based on the Pydantic model data.
        update: Updates a document identified by ObjectId with the data from the Pydantic model.
        delete: Removes a document from the collection by its unique ObjectId.
    """

    def __init__(
        self, client: AsyncIOMotorClient, collection_name: str, model_class: Type[M]
    ):
        """
        Initializes the service with the specified MongoDB client, database name, collection name, and model class
        Parameters:
            client (AsyncIOMotorClient): The MongoDB client instance to access the database.
            collection_name (str): The name of the database collection the service will interact with.
            model_class (Type[M]): The Pydantic model class for data validation and serialization.
        """
        self.db_name = mongo_settings.db
        self.db = AsyncIOMotorDatabase(client, self.db_name)
        self.collection = self.db.get_collection(collection_name)
        self.model_class = model_class

    async def get_all(self) -> List[M]:
        """Returns a list of all documents in the collection, each serialized into a Pydantic model."""
        documents = await self.collection.find().to_list(None)
        return [self.model_class.parse_obj(doc) for doc in documents]

    async def get_by_id(self, model_id: ObjectIdField) -> M | None:
        """Retrieves a document by its unique ObjectId, serialized into a Pydantic model."""
        document = await self.collection.find_one({"_id": model_id})
        if document:
            return self.model_class.parse_obj(document)

    async def create(self, model_schema: BaseModel) -> M:
        """Creates a new document in the collection based on the Pydantic model data and returns the created document."""
        document = model_schema.dict(by_alias=True, exclude_none=True)
        result = await self.collection.insert_one(document)
        document["_id"] = result.inserted_id
        return self.model_class.parse_obj(document)

    async def update(self, model_id: ObjectIdField, model_schema: M) -> M:
        """Updates a document identified by ObjectId with data from the Pydantic model."""  # TODO - fix return type
        document = model_schema.dict(by_alias=True, exclude_none=True)
        result = await self.collection.update_one({"_id": model_id}, {"$set": document})
        document["_id"] = ObjectId(result.upserted_id)
        document["acknowledged"] = result.acknowledged
        document["matched_count"] = result.matched_count
        document["modified_count"] = result.modified_count
        document["upserted_id"] = result.upserted_id
        return self.model_class.parse_obj(document)

    async def delete(self, model_id: ObjectIdField) -> dict[str, Any]:
        """Removes a document from the collection by its unique ObjectId."""  # TODO - fix return type
        result = await self.collection.delete_one({"_id": model_id})
        document = BaseDelete(
            _id=model_id,
            deleted_count=result.deleted_count,
            acknowledged=result.acknowledged,
        ).dict(by_alias=True, exclude_none=True)
        return document
