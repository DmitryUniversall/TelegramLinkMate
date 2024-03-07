from teleapi.core.orm.models.field import ModelField
from teleapi.core.orm.validators.generics.selection import SelectionValidator


class SelectionModelField(ModelField, SelectionValidator):
    pass
