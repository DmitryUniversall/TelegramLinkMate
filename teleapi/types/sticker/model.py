from typing import Optional
from teleapi.core.orm.models.generics.fields import IntegerModelField, StringModelField, BooleanModelField, RelatedModelField
from teleapi.types.filelike import FilelikeModel
from .sub_objects.sticker_type import StickerType
from teleapi.types.photo_size import PhotoSize
from teleapi.types.file import File
from teleapi.types.mask_position import MaskPosition


class StickerModel(FilelikeModel):
    type_: str = RelatedModelField(StickerType)
    width: int = IntegerModelField()
    height: int = IntegerModelField()
    is_animated: bool = BooleanModelField(default=False)
    is_video: bool = BooleanModelField(default=False)
    needs_repainting: bool = BooleanModelField(default=False)
    emoji: Optional[str] = StringModelField(is_required=False)
    set_name: Optional[str] = StringModelField(is_required=False)
    custom_emoji_id: Optional[str] = StringModelField(is_required=False)
    thumbnail: PhotoSize = RelatedModelField(PhotoSize, is_required=False)
    premium_animation: Optional[File] = RelatedModelField(File, is_required=False)
    mask_position: Optional[MaskPosition] = RelatedModelField(MaskPosition, is_required=False)
