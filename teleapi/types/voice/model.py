from typing import Optional
from teleapi.core.orm.models.generics.fields import IntegerModelField, StringModelField
from teleapi.types.filelike import FilelikeModel


class VoiceModel(FilelikeModel):
    duration: str = IntegerModelField()
    mime_type: Optional[str] = StringModelField(is_required=False)
