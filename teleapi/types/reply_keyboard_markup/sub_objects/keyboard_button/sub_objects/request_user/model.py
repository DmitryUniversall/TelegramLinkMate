from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import BooleanModelField, IntegerModelField


class KeyboardButtonRequestUserModel(Model):
    request_id: int = IntegerModelField()
    user_is_bot: bool = BooleanModelField(is_required=False)
    user_is_premium: bool = BooleanModelField(is_required=False)
