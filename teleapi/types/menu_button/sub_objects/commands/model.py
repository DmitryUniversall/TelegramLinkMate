from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import ConstantModelField


class MenuButtonCommandsModel(Model):
    type_: str = ConstantModelField("commands")
