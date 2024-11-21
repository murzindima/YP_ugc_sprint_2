from abc import ABC, abstractmethod

from pydantic import BaseModel

from queries.base import BaseFilter


class DataStorageService[M: BaseModel](ABC):
    """
    Abstract base class defining the interface for a data storage service.

    This class is designed to be subclassed for implementing specific data storage services
    that interact with different types of models using Pydantic for data validation.

    Attributes:
        - M (BaseModel): The Pydantic model type that the data storage service works with.
    """

    @abstractmethod
    async def get_by_id(self, model_id: str) -> M | None:
        """
        Abstract method to retrieve a model by its unique identifier.

        Parameters:
            - model_id (str): The unique identifier of the model.

        Returns:
            - M | None: The retrieved model if found, else None.
        """

    @abstractmethod
    async def get_all(self, model_filter: BaseFilter) -> list[M]:
        """
        Abstract method to retrieve a list of models based on a provided filter.

        Parameters:
            - model_filter (BaseFilter): An instance of BaseFilter or its subclass to apply filtering.

        Returns:
            - list[M]: A list of models matching the specified filter criteria.
        """
