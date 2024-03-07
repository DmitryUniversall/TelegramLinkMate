from teleapi.core.orm.models.field import ModelField
from teleapi.core.orm.validators.generics.typed import TypedValidator


class RelatedModelField(ModelField, TypedValidator):
    pass
