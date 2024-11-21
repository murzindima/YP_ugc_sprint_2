import abc
from typing import Any


class BaseStorage(abc.ABC):
    """
    Abstract base class for state storage.

    This class provides an interface for saving and retrieving state information.
    The actual method of storing the state is dependent on the implementation.
    For instance, the state can be stored in a database or in a distributed file system.
    This flexibility allows for various storage solutions to be integrated as needed.
    """

    @abc.abstractmethod
    def save_state(self, state: dict[str, Any]) -> None:
        """
        Save the given state to the storage.

        This method should be implemented to store the provided state dictionary in the
        chosen storage medium.
        The specifics of how the state is stored (e.g., serialization format,
        storage mechanism) are left to the implementation.

        Parameters:
        state (Dict[str, Any]): A dictionary representing the state to be saved.
        """

    @abc.abstractmethod
    def retrieve_state(self) -> dict[str, Any]:
        """
        Retrieve the state from storage.

        This method should be implemented to fetch the state information from storage.
        It should return a dictionary representing the state. The specifics of how the state
        is retrieved (e.g., deserialization format, retrieval mechanism) are left to the
        implementation.

        Returns:
        Dict[str, Any]: A dictionary representing the retrieved state.
        """
