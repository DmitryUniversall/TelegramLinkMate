import teleapi
from src.main.search.services.service import BaseService


class MusicalObjectModel(teleapi.orm.Model):
    service: BaseService = teleapi.orm.RelatedModelField(BaseService)
    url: str = teleapi.orm.StringModelField()
