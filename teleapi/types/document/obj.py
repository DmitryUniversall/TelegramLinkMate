from .model import DocumentModel
from teleapi.types.filelike import Filelike


class Document(DocumentModel, Filelike):
    pass
