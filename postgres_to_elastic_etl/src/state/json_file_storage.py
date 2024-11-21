import json
from logging import Logger

from .base_storage import BaseStorage


class JsonFileStorage(BaseStorage):
    """
    A JSON file-based implementation of the BaseStorage class.

    This class implements the storage of state information in a JSON file format.
    It provides methods to save and retrieve state data using JSON serialization,
    making it suitable for lightweight and human-readable state management.
    """

    def __init__(self, logger: Logger, file_path: str | None = "storage.json"):
        """
        Initialize the JsonFileStorage with a logger and a file path.

        This constructor sets up the storage system using a specified file path.
        If no file path is provided, it defaults to 'storage.json'. A logger is also
        initialized for logging purposes.

        Parameters:
        logger (Logger): A logger instance for logging events.
        file_path (Optional[str]): The path to the JSON file used for storing state.
                                   Defaults to 'storage.json'.
        """
        self.file_path = file_path
        self._logger = logger

    def save_state(self, state: dict) -> None:
        """
        Save the given state to a JSON file.

        Serializes the provided state dictionary into JSON format and writes it
        to the specified file. If the file does not exist, it will be created.

        Parameters:
        state (dict): A dictionary representing the state to be saved.
        """
        if self.file_path is None:
            raise ValueError("File path is not set.")
        with open(self.file_path, "w") as outfile:
            json.dump(state, outfile)

    def retrieve_state(self) -> dict:
        """
        Retrieve the state from a JSON file.

        Attempts to open and deserialize the state from the specified JSON file.
        If the file is not found or if the JSON is invalid, a warning is logged, and
        an empty dictionary is returned.

        Returns:
        dict: A dictionary representing the retrieved state, or an empty dictionary
              if the file does not exist or contains invalid JSON.
        """
        if self.file_path is None:
            raise ValueError("File path is not set.")
        try:
            with open(self.file_path) as json_file:
                return json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            self._logger.warning("No state file provided. Continue with default file.")
            return {}
