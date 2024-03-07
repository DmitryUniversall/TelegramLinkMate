from .model import AudioModel
from teleapi.types.filelike import Filelike


class Audio(AudioModel, Filelike):
    pass
