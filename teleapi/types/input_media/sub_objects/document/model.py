from teleapi.core.orm.models.generics.fields import BooleanModelField, ConstantModelField
from teleapi.types.input_media import InputMediaWithThumbnailModel


class InputMediaDocumentModel(InputMediaWithThumbnailModel):
    type_: str = ConstantModelField("document")
    disable_content_type_detection: bool = BooleanModelField(default=False)
