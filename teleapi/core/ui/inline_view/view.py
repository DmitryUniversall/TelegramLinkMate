import inspect
from abc import ABCMeta
from collections import defaultdict
from functools import wraps
from typing import List, Type

from teleapi.core.utils.collections import find_in_list
from teleapi.core.utils.collectors import CollectorMeta, collect_subclasses
from teleapi.core.utils.rand import generate_random_string
from teleapi.types.callback_query import CallbackQuery
from teleapi.types.inline_keyboard_markup import InlineKeyboardMarkup
from .button import BaseInlineViewButton
from teleapi.core.utils.syntax import default
from teleapi.core.ui.inline_view.button import button as button_factory


class InlineViewMeta(CollectorMeta, ABCMeta):
    _collector = {
        'func': collect_subclasses,
        'attributes': {
            BaseInlineViewButton: '__dynamic_buttons__'
        }
    }


class BaseInlineView(metaclass=InlineViewMeta):
    CALLBACK_DATA_FORMAT: str = "[{}={}]"
    __created_views__: List['BaseInlineView'] = []

    # Dynamic generated properties, that collects buttons(BaseInlineViewButton)
    __dynamic_buttons__: List[Type['BaseInlineViewButton']]

    __view_buttons__: List[Type['BaseInlineViewButton']] = []

    def __new__(cls, *args, **kwargs) -> 'BaseInlineView':
        instance = super().__new__(cls)
        BaseInlineView.__created_views__.append(instance)

        return instance

    def __init__(self) -> None:
        self.id = generate_random_string(5)

        self._buttons = [
            button_cls(self) for button_cls in (self.__class__.__dynamic_buttons__ + self.__class__.__view_buttons__)
        ]

        self.message = None

    @staticmethod
    def view_button(*, text: str, row: int = None, place: int = None, **meta_kwargs):
        def decorator(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError('You can use this decorator only with coroutine functions')

            @wraps(func)
            async def wrapper(btn, callback_query: 'CallbackQuery') -> None:
                return await func(btn.view, callback_query, button=btn)

            return button_factory(text=text, row=row, place=place, **meta_kwargs)(wrapper)

        return decorator

    def register_button(self, button: BaseInlineViewButton) -> None:
        if not isinstance(button, BaseInlineViewButton):
            raise TypeError("button must be instance of BaseInlineViewButton")

        self._buttons.append(button)

    def unregister_button(self, button: BaseInlineViewButton) -> None:
        self._buttons.remove(button)

    def get_sorted_buttons(self) -> List[List[BaseInlineViewButton]]:
        keyboard = defaultdict(list)

        for button in self._buttons:
            keyboard[button.row].insert(button.place, button)

        return [keyboard[key] for key in sorted(keyboard.keys())]

    async def make_markup(self) -> InlineKeyboardMarkup:
        for button in self._buttons:
            button.callback_data = self.__class__.CALLBACK_DATA_FORMAT.format(self.id, button.id) + (
                default(f"_{button.callback_data}", ""))

        return InlineKeyboardMarkup(inline_keyboard=self.get_sorted_buttons())

    async def on_click(self, button_id: str, callback_query: CallbackQuery) -> None:
        if self.message is None:
            self.message = callback_query.message

        button = find_in_list(self._buttons, lambda x: x.id == button_id)

        if button is not None:
            await button.on_click(callback_query)

        if not callback_query.is_answered:
            await callback_query.answer()


class View(BaseInlineView):
    pass
