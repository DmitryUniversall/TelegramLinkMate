from teleapi.core.executors.events import EventListener
from teleapi.types.update import Update
from abc import ABC


class OnetimeEventListener(EventListener, ABC):
    def after(self, update: Update, *args, **kwargs) -> None:
        self.is_active = False
