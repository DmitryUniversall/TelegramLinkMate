from typing import Optional
from teleapi.core.orm.models.generics.fields import StringModelField, RelatedModelField
from teleapi.types.filelike import FilelikeModel
from teleapi.types.photo_size import PhotoSize


class DocumentModel(FilelikeModel):
    thumbnail: Optional[str] = RelatedModelField(PhotoSize, is_required=False)
    file_name: Optional[str] = StringModelField(is_required=False)
    mime_type: Optional[str] = StringModelField(is_required=False)
