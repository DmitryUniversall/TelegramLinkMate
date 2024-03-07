from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import RelatedModelField, FloatModelField
from .sub_objects.mask_position_point import MaskPositionPoint


class MaskPositionModel(Model):
    point: str = RelatedModelField(MaskPositionPoint)
    x_shift: float = FloatModelField()
    y_shift: float = FloatModelField()
    scale: float = FloatModelField()
