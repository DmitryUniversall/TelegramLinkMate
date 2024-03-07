import os
from typing import Optional, Any

from teleapi.core.exceptions.generics import InvalidParameterError
# from teleapi.core.orm import ValidationError
from teleapi.core.orm.models import Model, ModelMeta
from teleapi.core.orm.models.generics.fields import InputFileModelField, StringModelField
from teleapi.core.utils.files import get_file
from teleapi.core.utils.syntax import default
from abc import ABCMeta, abstractmethod


class _InputFileModelMeta(ABCMeta, ModelMeta):
    pass


class InputFileModel(Model, metaclass=_InputFileModelMeta):
    data: Optional[bytes] = InputFileModelField(is_required=False)
    filename: str = StringModelField(is_required=False)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        if not hasattr(self, self.__file_field__):
            raise AttributeError(
                f"Declared __file_field__ '{self.__file_field__}' is not exists in class {self.__class__}"
            )

        if self.data:
            self.register_data(self.__file_field__, self.data, self.filename)
        elif self.__get_file_field_data() is not None and os.path.exists(self.__get_file_field_data()):
            data_filename, data = get_file(self.__get_file_field_data())
            filename = default(self.filename, data_filename)
            if not filename:
                raise InvalidParameterError(f"'filename' was not specified")
        # else:
        #     raise ValidationError(f"File data for {self} not specified")

    def register_data(self, field_name: str, data: bytes, filename: str) -> None:
        setattr(self, field_name, f"attach://{filename}")
        self.filename = filename
        self.data = data

    @property
    @abstractmethod
    def __file_field__(self) -> str:
        ...

    def __get_file_field_data(self) -> Any:
        return getattr(self, self.__file_field__)
