import os
from typing import List, Optional

from teleapi.core.orm.models.generics.fields import StringModelField, ConstantModelField, ListModelField, \
    RelatedModelField, InputFileModelField
from teleapi.core.utils.files import get_file
from teleapi.core.utils.syntax import default
from teleapi.enums.parse_mode import ParseMode
from teleapi.types.message_entity import MessageEntity
from teleapi.types.input_file import InputFileModel


class InputMediaModel(InputFileModel):
    __file_field__: str = "media"

    type_: str = ConstantModelField("UNKNOWN")  # OVERWRITE IN SUBCLASS
    media: str = StringModelField(is_required=False)
    caption: str = StringModelField(is_required=False)
    caption_entities: List[MessageEntity] = ListModelField(RelatedModelField(MessageEntity), is_required=False)
    parse_mode: ParseMode = RelatedModelField(ParseMode, is_required=False)

    data: Optional[bytes] = InputFileModelField(max_size="50MB", is_required=False)


class InputMediaWithThumbnailModel(InputMediaModel):
    thumbnail: str = StringModelField(is_required=False)
    thumbnail_data: bytes = InputFileModelField(max_size="200kB", is_required=False)
    thumbnail_filename: str = StringModelField(is_required=False)

    def __register_thumbnail(self, data: bytes, filename: str) -> None:
        self.thumbnail = f"attach://{filename}"
        self.thumbnail_data = data
        self.thumbnail_filename = filename

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        if self.thumbnail_data:
            self.__register_thumbnail(self.thumbnail_data, self.thumbnail_filename)

        if self.thumbnail is not None and os.path.exists(self.thumbnail):
            data_filename, data = get_file(self.thumbnail)
            filename = default(self.filename, data_filename)
            if not filename:
                raise ValueError(f"'filename' was not specified")

            self.__register_thumbnail(data, filename)
