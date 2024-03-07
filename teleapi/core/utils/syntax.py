from typing import Any


def default(value: Any, default_value: Any) -> Any:
    return value if value is not None else default_value
