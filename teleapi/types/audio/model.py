from typing import Optional
from teleapi.core.orm.models.generics.fields import IntegerModelField, StringModelField, RelatedModelField
from teleapi.types.filelike import FilelikeModel
from teleapi.types.photo_size import PhotoSize


class AudioModel(FilelikeModel):
    duration: int = IntegerModelField()
    thumbnail: Optional[PhotoSize] = RelatedModelField(PhotoSize, is_required=False)
    file_name: Optional[str] = StringModelField(is_required=False)
    mime_type: Optional[str] = StringModelField(is_required=False)
    performer: Optional[str] = StringModelField(is_required=False)
    title: Optional[str] = StringModelField(is_required=False)
