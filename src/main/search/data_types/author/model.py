import teleapi
from ..musical_object import MusicalObjectModel


class AuthorModel(MusicalObjectModel):
    name: str = teleapi.orm.StringModelField()
