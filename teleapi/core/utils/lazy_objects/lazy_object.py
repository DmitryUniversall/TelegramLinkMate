from abc import ABCMeta, abstractmethod
from typing import Any, Type
from functools import cached_property


class LazyObjectMeta(type, metaclass=ABCMeta):
    def __new__(mcs: Type['LazyObjectMeta'], cls_name: str, parents: tuple, dict_: dict) -> Type:
        dict_['obj'] = cached_property(dict_['obj'])
        dict_['obj'].__set_name__(dict_['obj'], 'obj')
        return super().__new__(mcs, cls_name, parents, dict_)


class LazyObject(metaclass=LazyObjectMeta):
    def __init__(self, data: Any) -> None:
        self.data = data

    @abstractmethod
    def obj(self): ...
