from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import ConstantModelField


class MenuButtonModel(Model):
    type_: str = ConstantModelField("UNKNOWN")  # OVERWRITE IN SUBCLASS
