from typing import Optional
from teleapi.core.orm.models.generics.fields import IntegerModelField, RelatedModelField
from teleapi.types.filelike import FilelikeModel
from teleapi.types.photo_size import PhotoSize


class VideoNoteModel(FilelikeModel):
    length: int = IntegerModelField()
    duration: str = IntegerModelField()
    thumbnail: Optional[str] = RelatedModelField(PhotoSize, is_required=False)
