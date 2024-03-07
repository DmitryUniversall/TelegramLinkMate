from .model import PhotoSizeModel
from teleapi.types.filelike import Filelike


class PhotoSize(PhotoSizeModel, Filelike):
    pass
