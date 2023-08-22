from typing import List, Optional, TYPE_CHECKING, Any
from ..author import Author
import teleapi
from ..musical_object import MusicalObjectModel
from ..data_source import DataSource

if TYPE_CHECKING:
    from .obj import Track


class TrackModel(MusicalObjectModel):
    variations: List['Track'] = teleapi.orm.ListModelField(teleapi.orm.RelatedModelField('src.main.search.data_types.track.obj.Track'), is_required=False)

    title: str = teleapi.orm.StringModelField()
    authors: List[Author] = teleapi.orm.ListModelField(teleapi.orm.RelatedModelField(Author))
    data_source: DataSource = teleapi.orm.RelatedModelField(DataSource)
    raw: Any = teleapi.orm.AnyTypeModelField()

    image_url: Optional[str] = teleapi.orm.StringModelField(is_required=False)
    duration: Optional[str] = teleapi.orm.StringModelField(is_required=False)
