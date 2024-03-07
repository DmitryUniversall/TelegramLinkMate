from teleapi.core.orm.models.generics.fields import IntegerModelField, BooleanModelField, ConstantModelField
from teleapi.types.input_media import InputMediaWithThumbnailModel


class InputMediaVideoModel(InputMediaWithThumbnailModel):
    type_: str = ConstantModelField("video")
    width: int = IntegerModelField(is_required=False)
    height: int = IntegerModelField(is_required=False)
    duration: int = IntegerModelField(is_required=False)
    supports_streaming: bool = BooleanModelField(default=False)
    has_spoiler: bool = BooleanModelField(default=False)
