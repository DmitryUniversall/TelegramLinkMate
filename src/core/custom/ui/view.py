from typing import Optional, List, TYPE_CHECKING

import teleapi
from .exceptions import ViewHasNoMessageError
from abc import abstractmethod, ABC
from teleapi.core.ui.inline_view.view import BaseInlineView

if TYPE_CHECKING:
    from .button import CustomButton


class CustomUIView(teleapi.View, ABC):
    def __init__(self, initial_message: Optional[teleapi.Message] = None) -> None:
        super().__init__()

        self.message = initial_message

    async def stop(self) -> None:
        try:
            BaseInlineView.__created_views__.remove(self)
        except ValueError:  # was not registered
            return

    def add_buttons(self, buttons: List[List['CustomButton']]) -> None:
        for row, row_buttons in enumerate(buttons):
            for place, button in enumerate(row_buttons):
                button.row = row
                button.place = place

                self.register_button(button)

    def clear_items(self) -> None:
        self._buttons.clear()

    def set_layout(self, layout: List[List['CustomButton']]) -> None:
        self.clear_items()
        self.add_buttons(layout)

    async def update(self, **kwargs) -> None:
        if self.message is None:
            raise ViewHasNoMessageError(f"You must specify message for view {self.__class__.__name__} to use this")

        await self.self_edit(**kwargs)

    async def delete(self, **kwargs) -> None:
        if self.message is None:
            raise ViewHasNoMessageError(f"You must specify message for view {self.__class__.__name__} to use this")

        await self.message.delete(**kwargs)
        self.message = None
        await self.stop()

    @abstractmethod
    async def self_edit(self, **kwargs) -> None: ...

    @abstractmethod
    async def reply(self, message: teleapi.Message, **kwargs) -> teleapi.Message: ...

    @abstractmethod
    async def send(self, chat: teleapi.Chat, **kwargs) -> teleapi.Message: ...
