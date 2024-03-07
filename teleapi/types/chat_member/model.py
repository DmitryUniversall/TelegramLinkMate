from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import RelatedModelField, ConstantModelField
from teleapi.types.user import User


class ChatMemberModel(Model):
    status: str = ConstantModelField("member")
    user: User = RelatedModelField(User)
