from teleapi.core.orm.validators.generics.input_file import InputFileValidator
from teleapi.core.orm.models.field import ModelField


class InputFileModelField(ModelField, InputFileValidator):
    pass
