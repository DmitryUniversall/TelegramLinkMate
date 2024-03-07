from typing import Optional

import teleapi
from src.core.custom import CustomUIView


class ErrorMessageView(CustomUIView):
    def __init__(self, error_message: Optional[str], **kwargs) -> None:
        super().__init__(**kwargs)

        self.error_message = error_message

    def _get_error_message_text(self) -> str:
        return teleapi.project_settings.STRINGS.errors.error_message_exception(error_message=self.error_message)

    def _get_unknown_error_message_text(self) -> str:
        return teleapi.project_settings.STRINGS.errors.unknown_error

    async def _get_text(self) -> str:
        return self._get_error_message_text() if self.error_message is not None else self._get_unknown_error_message_text()

    async def self_edit(self, **kwargs) -> None:
        await self.message.edit_text(
            text=await self._get_text(),
            view=self,
            **kwargs
        )

    async def reply(self, message: teleapi.Message, **kwargs) -> teleapi.Message:
        return await self.message.edit_text(  # type: ignore
            text=await self._get_text(),
            view=self,
            **kwargs
        )

    async def send(self, chat: teleapi.Chat, **kwargs) -> teleapi.Message:
        return await chat.send_message(
            text=await self._get_text(),
            view=self,
            parse_mode=teleapi.ParseMode.HTML,
            **kwargs
        )
