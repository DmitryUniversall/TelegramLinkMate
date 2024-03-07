import teleapi
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .view import CustomUIView


class CustomButton(teleapi.InlineViewButton):
    def __init__(self, view: 'CustomUIView', row: int = 0, place: int = 0, **kwargs) -> None:
        super().__init__(view, row=row, place=place, **kwargs)
