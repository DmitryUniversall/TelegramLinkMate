from functools import partial
from typing import List, Any


def filter_attributes(obj, condition, safe: bool = True) -> List[Any]:
    objects = []

    for attr in filter(lambda x: not x.startswith("__") if safe else True, dir(obj)):
        value = getattr(obj, attr)

        if condition(value):
            objects.append(value)

    return objects


def collect_subclasses(type_, obj, safe: bool = True):
    return filter_attributes(obj, lambda value: isinstance(value, type) and issubclass(value, type_), safe=safe)


def collect_instances(type_, obj, safe: bool = True):
    return filter_attributes(obj, lambda value: isinstance(value, type_), safe=safe)


class CollectorMeta(type):
    """
    _collector: dict = {
        "func": collect_subclasses, :type Callable[[type, Any], List[Any]]
        "attributes": {
            <TYPE>: <ATTRIBUTE_NAME>
        }
    }
    """
    _collector: dict = {}

    def __new__(mcs, name: str, parents: tuple, attrs: dict) -> type:
        func = mcs._collector.get('func', None)
        attributes = mcs._collector.get('attributes', None)

        if not (func is not None and attributes is not None):
            raise KeyError("To use collector you must define 'func' and 'attributes' fields in '_collector'")

        cls = super().__new__(mcs, name, parents, attrs)

        for type_, attribute in attributes.items():
            setattr(mcs, attribute, property(partial(func, (type_, cls))))

        return cls
