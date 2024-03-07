from teleapi.core.orm.models.generics.fields import BooleanModelField, ConstantModelField
from teleapi.types.input_media import InputMediaModel


class InputMediaPhotoModel(InputMediaModel):
    type_: str = ConstantModelField("photo")
    has_spoiler: bool = BooleanModelField(default=False)
