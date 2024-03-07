from typing import Optional

from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import StringModelField, BooleanModelField, RelatedModelField

from .sub_objects.poll_type import KeyboardButtonPollType
from .sub_objects.request_chat import KeyboardButtonRequestChat
from .sub_objects.request_user import KeyboardButtonRequestUser
from teleapi.types.web_app_info import WebAppInfo


class KeyboardButtonModel(Model):
    text: str = StringModelField()
    request_contact: Optional[bool] = BooleanModelField(is_required=False)
    request_location: Optional[bool] = BooleanModelField(is_required=False)
    request_user: Optional[KeyboardButtonRequestUser] = RelatedModelField(KeyboardButtonRequestUser, is_required=False)
    request_chat: Optional[KeyboardButtonRequestChat] = RelatedModelField(KeyboardButtonRequestChat, is_required=False)
    request_poll: Optional[KeyboardButtonPollType] = RelatedModelField(KeyboardButtonPollType, is_required=False)
    web_app: Optional[WebAppInfo] = RelatedModelField(WebAppInfo, is_required=False)
