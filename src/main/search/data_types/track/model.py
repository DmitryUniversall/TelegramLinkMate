from typing import List, Optional, TYPE_CHECKING
from ..author import Author
import teleapi
from ..musical_object import MusicalObjectModel

if TYPE_CHECKING:
    from .obj import Track


class TrackModel(MusicalObjectModel):
    title: str = teleapi.orm.StringModelField()
    authors: List[Author] = teleapi.orm.RelatedModelField(Author)
    audio_sources: List[str] = teleapi.orm.ListModelField(teleapi.orm.StringModelField(), default=[])
    variations: List['Track'] = teleapi.orm.ListModelField(teleapi.orm.RelatedModelField('src.main.search.data_types.track.obj.Track'), is_required=False)

    duration: Optional[str] = teleapi.orm.StringModelField(is_required=False)
