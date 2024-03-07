from typing import Optional
from teleapi.core.orm.models.generics.fields import StringModelField
from teleapi.types.filelike import FilelikeModel


class FileModel(FilelikeModel):
    file_path: Optional[str] = StringModelField()
