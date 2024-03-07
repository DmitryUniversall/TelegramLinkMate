from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import ConstantModelField, StringModelField, RelatedModelField
from teleapi.types.web_app_info import WebAppInfo


class MenuButtonWebAppModel(Model):
    type_: str = ConstantModelField("web_app")
    text: str = StringModelField()
    web_app: WebAppInfo = RelatedModelField(WebAppInfo)
