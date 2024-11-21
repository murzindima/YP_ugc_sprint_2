from typing import Type

from pydantic import BaseModel
from pydantic_mongo import ObjectIdField

from src.schemas.base import BaseDelete
from src.services.data_repository.mongo import MongoService


class BaseService[M: BaseModel]:
    """Base service class for working at the business logic and validation level using Pydantic."""

    def __init__(
        self,
        model_schema_class: Type[M],
        mongo_service: MongoService,
    ):
        self.model_schema_class = model_schema_class
        self.mongo_service = mongo_service

    async def get_all_models(self) -> list[M]:
        """Retrieve multiple models."""
        db_models = await self.mongo_service.get_all()

        return [self.model_schema_class.model_validate(model) for model in db_models]

    async def get_model_by_id(self, model_id: ObjectIdField) -> M | None:
        """Retrieve a model by identifier."""
        db_model = await self.mongo_service.get_by_id(model_id)
        if not db_model:
            return None

        return self.model_schema_class.model_validate(db_model)

    async def create_model(self, model_schema: M) -> M:
        """Create a model."""
        db_model = await self.mongo_service.create(model_schema)
        return self.model_schema_class.model_validate(db_model)

    async def update_model(self, model_id: ObjectIdField, new_data: M) -> M:
        """Update a model by identifier."""
        db_model = await self.mongo_service.update(model_id, new_data)
        return self.model_schema_class.model_validate(db_model)

    async def delete_model(self, model_id: ObjectIdField) -> BaseDelete:
        """Delete a model by identifier."""
        db_model = await self.mongo_service.delete(model_id)
        model_schema_class = BaseDelete(**db_model)
        return model_schema_class
