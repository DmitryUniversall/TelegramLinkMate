import inspect
from typing import TYPE_CHECKING
from teleapi.types.inline_keyboard_markup.sub_objects import InlineKeyboardButton
from teleapi.core.utils.collections import clear_none_values
from teleapi.core.utils.rand import generate_random_string
from teleapi.core.utils.syntax import default

if TYPE_CHECKING:
    from .view import BaseInlineView
    from teleapi.types.callback_query import CallbackQuery


class BaseInlineViewButton(InlineKeyboardButton):
    class Meta:
        pass

    def __init__(self, view: 'BaseInlineView', row: int = None, place: int = None, **kwargs) -> None:
        self.id = generate_random_string(5)
        self.view = view

        self.row = default(row, getattr(self.__class__.Meta, "row", None))
        self.place = default(place, getattr(self.__class__.Meta, "place", -1))

        if self.row is None:
            raise AttributeError(f"Unable to get '{self}' button row")

        meta_kwargs = {}
        for field in self.__class__.__fields__:
            if field.__attribute_name__ not in kwargs.keys() and (value := getattr(self.__class__.Meta, field.__attribute_name__, None)):
                meta_kwargs[field.__attribute_name__] = value

        super().__init__(**kwargs, **meta_kwargs)

    async def on_click(self, callback_query: 'CallbackQuery') -> None:
        ...


class InlineViewButton(BaseInlineViewButton):
    pass


def button(*, text: str, row: int = None, place: int = None, **meta_kwargs):
    def decorator(func):
        if not inspect.iscoroutinefunction(func):
            raise TypeError('You can use this decorator only with coroutine functions')

        meta = type("Meta", (object,), clear_none_values({'text': text, 'row': row, 'place': place, **meta_kwargs}))

        button_cls = type(func.__name__, (InlineViewButton,), {
            "on_click": func,
            "Meta": meta
        })

        return button_cls

    return decorator
