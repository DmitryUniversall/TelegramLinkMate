from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import StringModelField


class WriteAccessAllowedModel(Model):
    web_app_name: str = StringModelField()
