from .model import VoiceModel
from teleapi.types.filelike import Filelike


class Voice(VoiceModel, Filelike):
    pass
