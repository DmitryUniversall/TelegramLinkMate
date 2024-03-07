from abc import ABC, abstractmethod
from typing import Any


class Validateable(ABC):
    @abstractmethod
    def validate(self, value: Any) -> Any:
        ...
