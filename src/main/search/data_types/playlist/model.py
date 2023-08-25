import teleapi
from typing import Optional, List
from ..track import Track
from ..musical_object import MusicalObjectModel


class PlaylistModel(MusicalObjectModel):
    title: str = teleapi.orm.StringModelField()
    tracks: List[Track] = teleapi.orm.ListModelField(teleapi.orm.RelatedModelField(Track), default=[])
    image_url: Optional[str] = teleapi.orm.StringModelField(default="https://2.bp.blogspot.com/-I20F9JVpz2c/XDGqLood6dI/AAAAAAAACpw/OkSbmANTIPgC_af_ZC0hztGWRLK-TvlOgCLcBGAs/s640/sound-waves-moving-graphic-illustration_hzbxvpdyg_thumbnail-full07.png")
