from typing import Any

from .base_storage import BaseStorage


class State:
    """
    A class for managing state during data migration processes.

    This class is designed to handle the state of a data migration or a similar process.
    It uses an instance of `BaseStorage` to persist and retrieve state information.
    This allows for state data to be maintained across different stages of the process.
    """

    def __init__(self, storage: BaseStorage):
        """
        Initialize the State object with a storage mechanism.

        The constructor accepts an instance of `BaseStorage` which is used for
        persisting and retrieving the state data.

        Parameters:
        storage (BaseStorage): An instance of a class that implements the BaseStorage
                               interface, used for storing and retrieving state data.
        """
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """
        Set a state value in the storage.

        This method allows for setting a value associated with a specific key in the
        storage.
        If the key already exists, its value will be updated.

        Parameters:
        key (str): The key under which the value should be stored.
        value (Any): The value to be stored.
        """
        state = self.storage.retrieve_state()
        state[key] = value
        self.storage.save_state(state)

    def get_state(self, key: str) -> Any:
        """
        Retrieve a state value from the storage.

        This method fetches the value associated with the specified key from the storage.
        If the key does not exist, it returns None.

        Parameters:
        key (str): The key whose value needs to be retrieved.

        Returns:
        Any: The value associated with the given key, or None if the key does not exist.
        """
        return self.storage.retrieve_state().get(key)
