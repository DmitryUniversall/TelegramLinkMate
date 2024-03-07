from typing import Optional
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField, FloatModelField


class LocationModel(Model):
    longitude: float = FloatModelField()
    latitude: float = FloatModelField()
    horizontal_accuracy: Optional[float] = FloatModelField(is_required=False, min_value=0, max_value=1500)
    live_period: Optional[int] = IntegerModelField(is_required=False)
    heading: Optional[int] = IntegerModelField(is_required=False)
    proximity_alert_radius: Optional[int] = IntegerModelField(is_required=False, min_value=0, max_value=360)
