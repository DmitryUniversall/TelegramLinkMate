from typing import Optional, List
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import StringModelField, BooleanModelField, RelatedModelField, ListModelField
from teleapi.types.sticker.sub_objects.sticker_type import StickerType

from teleapi.types.sticker import Sticker
from teleapi.types.photo_size import PhotoSize


class StickerSetModel(Model):
    name: str = StringModelField()
    title: str = StringModelField()
    sticker_type: StickerType = RelatedModelField(StickerType)
    stickers: List[Sticker] = ListModelField(Sticker)
    is_animated: bool = BooleanModelField(default=False)
    is_video: bool = BooleanModelField(default=False)
    thumbnail: Optional[PhotoSize] = RelatedModelField(PhotoSize, is_required=False)
