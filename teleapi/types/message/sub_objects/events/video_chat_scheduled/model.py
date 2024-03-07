from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import UnixTimestampModelField
from datetime import datetime


class VideoChatScheduledModel(Model):
    start_date: datetime = UnixTimestampModelField()
