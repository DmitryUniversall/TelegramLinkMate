from typing import List
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField, ListModelField, RelatedModelField
from teleapi.types.photo_size import PhotoSize


class UserProfilePhotosModel(Model):
    total_count: int = IntegerModelField()
    photos: List[List[PhotoSize]] = ListModelField(ListModelField(RelatedModelField(PhotoSize)))
