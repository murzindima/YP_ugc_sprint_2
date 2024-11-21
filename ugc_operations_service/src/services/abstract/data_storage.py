from abc import ABC, abstractmethod
from typing import List
from uuid import UUID


class DataStorageService[M](ABC):
    """
    Abstract base class defining the interface for a data storage service.

    This class is designed to be subclassed for implementing specific data storage services
    that interact with different types of models.
    """

    @abstractmethod
    async def get_all(self) -> List[M]:
        """Abstract method to retrieve a list of models."""

    @abstractmethod
    async def get_by_id(self, model_id: UUID) -> M | None:
        """Abstract method to retrieve a model by its unique identifier."""
