from teleapi.core.orm.models.generics.fields import IntegerModelField
from teleapi.types.filelike import FilelikeModel


class PhotoSizeModel(FilelikeModel):
    width: int = IntegerModelField()
    height: int = IntegerModelField()
