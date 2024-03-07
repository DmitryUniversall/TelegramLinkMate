from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import RelatedModelField, StringModelField
from teleapi.types.location.obj import Location


class ChatLocationModel(Model):
    location: Location = RelatedModelField(Location)
    address: str = StringModelField(min_size=1, max_size=64)
