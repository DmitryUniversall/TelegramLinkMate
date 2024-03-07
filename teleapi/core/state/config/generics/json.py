import json
from typing import Any, Dict

from teleapi.core.state.config.abc import AbstractConfig


class JsonFileConfig(AbstractConfig):
    """
    Represents a configuration class that uses a JSON file for storing settings.
    Note: File will not be modified during settings update

    Methods:
    - `__init__(self, path: str) -> None`
        Initializes the JsonFileConfig instance

    - `load(self) -> Dict[str, Any]`
         Load data from the specified JSON file.
    """

    def __init__(self, path: str) -> None:
        """
        Initializes the JsonFileConfig instance by loading data from the specified JSON file.

        :param path: `str`
            The path to the JSON file.
        """

        self._file_path = path

    def load(self) -> Dict[str, Any]:
        """
        Loads and returns configuration data from the specified JSON file.

        :return: `Dict[str, Any]`
            A dictionary containing configuration data.
        """

        with open(self._file_path, "r") as file:
            return json.load(file)
