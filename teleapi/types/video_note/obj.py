from .model import VideoNoteModel
from teleapi.types.filelike import Filelike


class VideoNote(VideoNoteModel, Filelike):
    pass
