from typing import Optional
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField, StringModelField


class FilelikeModel(Model):
    file_id: str = StringModelField()
    file_unique_id: str = StringModelField()
    file_size: Optional[int] = IntegerModelField(is_required=False)
