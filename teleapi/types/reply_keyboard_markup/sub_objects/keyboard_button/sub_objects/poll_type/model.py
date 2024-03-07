from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import StringModelField


class KeyboardButtonPollTypeModel(Model):
    type_: str = StringModelField(is_required=False)
