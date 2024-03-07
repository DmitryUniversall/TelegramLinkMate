from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField, RelatedModelField
from teleapi.types.user import User


class ProximityAlertTriggeredModel(Model):
    traveler: User = RelatedModelField(User)
    watcher: User = RelatedModelField(User)
    distance: int = IntegerModelField()
