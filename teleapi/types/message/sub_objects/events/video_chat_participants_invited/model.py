from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import ListModelField, RelatedModelField
from teleapi.types.user import User
from typing import List


class VideoChatParticipantsInvitedModel(Model):
    users: List[User] = ListModelField(RelatedModelField(User))
