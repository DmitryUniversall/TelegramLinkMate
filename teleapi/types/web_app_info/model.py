from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import StringModelField


class WebAppInfoModel(Model):
    url = StringModelField(validate=lambda x: None if x.startswith("https://") else "Bad WebAppInfo url (must starts with https://)")
