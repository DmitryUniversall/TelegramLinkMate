from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField


class UserSharedModel(Model):
    request_id: int = IntegerModelField()
    user_id: int = IntegerModelField()
