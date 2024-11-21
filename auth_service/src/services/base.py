from typing import Type
from uuid import UUID

from pydantic import BaseModel

from src.services.data_repository.postgres import PostgresService


class BaseService[M: BaseModel]:
    """Base service class for working at the business logic and validation level using Pydantic."""

    def __init__(
        self,
        model_schema_class: Type[M],
        postgres_service: PostgresService,
    ):
        self.model_schema_class = model_schema_class
        self.postgres_service = postgres_service

    async def get_all_models(self) -> list[M]:
        """Retrieve multiple models."""
        db_models = await self.postgres_service.get_all()

        return [self.model_schema_class.model_validate(model) for model in db_models]

    async def get_model_by_id(self, model_id: UUID) -> M | None:
        """Retrieve a model by identifier."""
        db_model = await self.postgres_service.get_by_id(model_id)
        if not db_model:
            return None

        return self.model_schema_class.model_validate(db_model)

    async def create_model(self, model_schema: M) -> M:
        """Create a model."""
        db_model = await self.postgres_service.create(model_schema)
        return self.model_schema_class.model_validate(db_model)

    async def update_model(self, model_id: UUID, new_data: M) -> M | None:
        """Update a model by identifier."""
        db_model = await self.postgres_service.update(model_id, new_data)
        if not db_model:
            return None

        return self.model_schema_class.model_validate(db_model)

    async def delete_model(self, model_id: UUID) -> M | None:
        """Delete a model by identifier."""
        db_model = await self.postgres_service.delete(model_id)
        if not db_model:
            return None

        return self.model_schema_class.model_validate(db_model)
