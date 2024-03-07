from typing import List
from teleapi.core.orm.models.field import BaseModelField
from teleapi.core.utils.collectors import CollectorMeta, collect_instances


class ModelMeta(CollectorMeta):
    _collector: dict = {
        'func': collect_instances,
        'attributes': {
            BaseModelField: '__fields__'
        }
    }


class BaseModel(metaclass=ModelMeta):
    # Dynamic generated property that collects fields(BaseModelField)
    __fields__: List[BaseModelField]

    def __init__(self, **kwargs) -> None:
        for field in self.__class__.__fields__:
            setattr(self, field.__attribute_name__, kwargs.get(field.__attribute_name__, None))

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} [{'; '.join([f'{field.__attribute_name__}[{getattr(self, field.__attribute_name__, None)}]' for field in self.__class__.__fields__])}]>"

    def self_validate(self) -> None:
        for field in self.__class__.__fields__:
            field.validate(getattr(self, field.__attribute_name__))


class Model(BaseModel):
    pass
