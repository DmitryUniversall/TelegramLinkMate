import teleapi
from typing import Optional, List
from ..track import Track
from ..musical_object import MusicalObjectModel


class PlaylistModel(MusicalObjectModel):
    title: str = teleapi.orm.StringModelField()
    tracks: List[Track] = teleapi.orm.ListModelField(teleapi.orm.RelatedModelField(Track), default=[])
    image_url: Optional[str] = teleapi.orm.StringModelField(is_required=False)
