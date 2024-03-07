from teleapi.core.orm.models.generics.fields import IntegerModelField, BooleanModelField, ConstantModelField
from teleapi.types.input_media import InputMediaWithThumbnailModel


class InputMediaAnimationModel(InputMediaWithThumbnailModel):
    type_: str = ConstantModelField("animation")
    width: int = IntegerModelField(is_required=False)
    height: int = IntegerModelField(is_required=False)
    duration: int = IntegerModelField(is_required=False)
    has_spoiler: bool = BooleanModelField(default=False)
