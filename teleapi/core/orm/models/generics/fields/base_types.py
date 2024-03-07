from teleapi.core.orm.validators.generics.base_types import BooleanValidator, IntegerValidator, StringValidator, DatetimeValidator, FloatValidator
from teleapi.core.orm.models.field import ModelField


class UnixTimestampModelField(ModelField, DatetimeValidator):
    pass


class BooleanModelField(ModelField, BooleanValidator):
    pass


class IntegerModelField(ModelField, IntegerValidator):
    pass


class StringModelField(ModelField, StringValidator):
    pass


class FloatModelField(ModelField, FloatValidator):
    pass
