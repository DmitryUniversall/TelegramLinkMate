from .model import VideoModel
from teleapi.types.filelike import Filelike


class Video(VideoModel, Filelike):
    pass
