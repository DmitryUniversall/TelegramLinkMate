from typing import Union, Dict, List

JsonValue = Union[Dict[str, 'JsonFieldValue'], List['JsonFieldValue'], bool, str, int, float, None]
