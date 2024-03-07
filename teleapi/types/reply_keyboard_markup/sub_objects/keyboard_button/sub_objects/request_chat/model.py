from typing import Optional

from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import (
    BooleanModelField,
    RelatedModelField,
    IntegerModelField
)
from teleapi.types.chat_permissions.sub_objects.chat_administrator_rights import ChatAdministratorRights


class KeyboardButtonRequestChatModel(Model):
    request_id: int = IntegerModelField()
    chat_is_channel: bool = BooleanModelField(is_required=False)
    chat_is_forum: bool = BooleanModelField(is_required=False)
    chat_has_username: bool = BooleanModelField(is_required=False)
    chat_is_created: bool = BooleanModelField(is_required=False)
    bot_is_member: bool = BooleanModelField(is_required=False)

    user_administrator_rights: Optional[ChatAdministratorRights] = RelatedModelField(ChatAdministratorRights, is_required=False)
    bot_administrator_rights: Optional[ChatAdministratorRights] = RelatedModelField(ChatAdministratorRights, is_required=False)
