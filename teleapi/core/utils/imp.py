import importlib
from functools import lru_cache
from typing import Any


@lru_cache(maxsize=None)
def import_module(name: str, package=None):
    """
    Функция для получения объекта модуля по названию (с кэшом)
    """
    return importlib.import_module(name, package=package)


@lru_cache(maxsize=None)
def import_object(from_: str) -> Any:
    """
    Функция для получения объекта из модуля по названию (с кэшом)

    :param from_: str
        путь до объекта в формате '*.<module_name>.<object_name>'
    """
    return getattr(import_module('.'.join(from_.split(".")[:-1])), from_.split(".")[-1])
