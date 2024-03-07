from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import ConstantModelField


class MenuButtonDefaultModel(Model):
    type_: str = ConstantModelField("default")
