from typing import List
import teleapi


class DataSourceModel(teleapi.orm.Model):
    audio_source: List[str] = teleapi.orm.ListModelField(teleapi.orm.StringModelField(), default=[])
    video_source: List[str] = teleapi.orm.ListModelField(teleapi.orm.StringModelField(), default=[])
