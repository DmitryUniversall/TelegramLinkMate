from teleapi.core.orm.models.generics.fields import StringModelField
from teleapi.core.orm.models import Model


class WebAppDataModel(Model):
    data: str = StringModelField()
    button_text: str = StringModelField()
