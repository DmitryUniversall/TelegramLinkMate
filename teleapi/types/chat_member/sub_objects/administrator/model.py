from teleapi.core.orm.models.generics.fields import StringModelField, BooleanModelField, ConstantModelField
from teleapi.types.chat_member import ChatMemberModel
from teleapi.types.chat_permissions.sub_objects.chat_administrator_rights import ChatAdministratorRightsModel
from typing import Optional


class ChatAdministratorModel(ChatMemberModel, ChatAdministratorRightsModel):
    status: str = ConstantModelField("administrator")
    custom_title: Optional[str] = StringModelField(is_required=False)
    can_be_edited: bool = BooleanModelField(default=False)
