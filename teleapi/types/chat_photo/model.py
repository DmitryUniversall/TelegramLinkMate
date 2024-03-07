from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import StringModelField


class ChatPhotoModel(Model):
    small_file_id: str = StringModelField()
    small_file_unique_id: str = StringModelField()
    big_file_id: str = StringModelField()
    big_file_unique_id: str = StringModelField()
