import teleapi
from typing import Optional, List

from ..track.obj import Track
from ...services.service import BaseService


class PlaylistModel(teleapi.orm.Model):
    tracks: List[Track] = teleapi.orm.ListModelField(teleapi.orm.RelatedModelField(Track), default=[])
    image_url: Optional[str] = teleapi.orm.StringModelField(is_required=False)
    service: BaseService = teleapi.orm.RelatedModelField(BaseService)
