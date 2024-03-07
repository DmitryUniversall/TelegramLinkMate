from .lazy_object import LazyObject
from teleapi.core.utils.imp import import_module, import_object


class LazyModule(LazyObject):
    def obj(self):
        return import_module(self.data)


class LazyModuleObject(LazyObject):
    def obj(self):
        return import_object(self.data)
