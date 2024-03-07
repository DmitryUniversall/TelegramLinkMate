from teleapi.core.orm.validators.generics.list_ import ListValidator
from teleapi.core.orm.models.field import ModelField


class ListModelField(ModelField, ListValidator):
    pass
