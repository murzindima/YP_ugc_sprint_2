from typing import Type
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import Base
from src.services.abstract.data_storage import DataStorageService


class PostgresCrudService[M: Base](DataStorageService):
    """A base class for CRUD operations on models stored in a Postgres database."""

    def __init__(self, session: AsyncSession, model_class: Type[M]):
        self.session = session
        self.model_class = model_class

    async def get_all(self) -> list[M]:
        """Retrieve multiple models."""
        async with self.session.begin():
            models = await self.session.execute(select(self.model_class))
            return models.unique().scalars().all()

    async def get_by_id(self, model_id: UUID) -> M | None:
        """Retrieve a model by identifier."""
        async with self.session.begin():
            model = await self.session.get(self.model_class, model_id)
            return model

    async def create(self, model_schema: BaseModel) -> M:
        """Create a model."""
        model_instance = self.model_class(**model_schema.model_dump())
        self.session.add(model_instance)
        await self.session.commit()
        return model_instance

    async def update(self, model_id: UUID, model_schema: BaseModel) -> M | None:
        """Update a model by identifier."""
        model_data = model_schema.model_dump(exclude_none=True)
        async with self.session.begin():
            model = await self.session.get(self.model_class, model_id)
            if model is None:
                return None

            if model_data:
                await self.session.execute(
                    update(self.model_class)
                    .where(self.model_class.id == model_id)
                    .values(model_data)
                )
                self.session.expire_all()

            return await self.session.get(self.model_class, model_id)

    async def delete(self, model_id: UUID) -> M | None:
        """Delete a model by identifier."""
        async with self.session.begin():
            result = await self.session.execute(
                delete(self.model_class)
                .where(self.model_class.id == model_id)
                .returning(self.model_class)
            )
            return result.scalar()
