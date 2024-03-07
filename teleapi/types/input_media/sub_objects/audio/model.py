from teleapi.core.orm.models.generics.fields import IntegerModelField, StringModelField, ConstantModelField
from teleapi.types.input_media import InputMediaWithThumbnailModel


class InputMediaAudioModel(InputMediaWithThumbnailModel):
    type_: str = ConstantModelField("audio")
    duration: int = IntegerModelField(is_required=False)
    performer: str = StringModelField(is_required=False)
