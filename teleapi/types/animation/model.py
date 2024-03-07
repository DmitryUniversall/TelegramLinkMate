from typing import Optional
from teleapi.core.orm.models.generics.fields import IntegerModelField, StringModelField, RelatedModelField
from teleapi.types.filelike import FilelikeModel
from teleapi.types.photo_size import PhotoSize


class AnimationModel(FilelikeModel):
    width: int = IntegerModelField()
    height: int = IntegerModelField()
    duration: str = IntegerModelField()
    thumbnail: Optional[PhotoSize] = RelatedModelField(PhotoSize, is_required=False)
    file_name: Optional[str] = StringModelField(is_required=False)
    mime_type: Optional[str] = StringModelField(is_required=False)
