from typing import Any, Dict
from abc import ABC, abstractmethod


class AbstractConfig(ABC):
    """
    Abstract base class for configuration classes.

    Methods:
    - `load(self) -> Dict[str, Any]` (Abstract)
        Abstract method to load and return configuration data.
    """

    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """
        Abstract method to be implemented by subclasses.
        Loads and returns configuration data.

        :return: `Dict[str, Any]`
            A dictionary containing configuration data.
        """
