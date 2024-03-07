from teleapi.core.utils.collections import replace_substring
from .model import MessageEntityModel
from typing import List, Tuple
import re


class MessageEntity(MessageEntityModel):
    @classmethod
    async def parse(cls, string: str) -> Tuple[str, List['MessageEntity']]:
        entities = []

        while match := re.search('<(\w+)>>(\S+)>', string):
            type_, text = match.groups()
            string = replace_substring(string, match.start(), match.end(), text)

            entities.append(
                MessageEntity(
                    type_=type_,
                    offset=match.start(),
                    length=len(text)
                )
            )

        return string, entities
