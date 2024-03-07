from typing import Optional, List
from teleapi.core.orm.models.generics.fields import InputFileModelField, RelatedModelField, StringModelField, ListModelField
from teleapi.types.mask_position import MaskPosition
from teleapi.types.input_file import InputFileModel


class InputStickerModel(InputFileModel):
    __file_field__: str = "sticker"

    sticker: str = StringModelField(is_required=False)
    emoji_list: List[str] = ListModelField(StringModelField(max_size=2024), is_required=False, min_size=1, max_size=20)
    keywords: List[str] = ListModelField(StringModelField(max_size=64), is_required=False, max_size=20, default=[])
    mask_position: Optional[MaskPosition] = RelatedModelField(MaskPosition, is_required=False)

    data: Optional[bytes] = InputFileModelField(max_size="50MB", is_required=False)
