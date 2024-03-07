from .model import AnimationModel
from teleapi.types.filelike import Filelike


class Animation(AnimationModel, Filelike):
    pass
