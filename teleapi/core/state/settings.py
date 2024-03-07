import os
from typing import Any, Dict, Optional
from .exceptions import ConfigurationError
from teleapi.core.utils.lazy_objects import LazyObject
from .config import AbstractConfig, PyModuleConfig


class ProjectSettings:
    """
    Manages project settings using various configurations (used in `setup_from_environment` method)

    Class Attributes:
    - `ENVIRONMENT_VARIABLE: str`
        The environment variable used to specify the configuration module.

    - `LAZY_OBJECT_PREFIX: str`
        Prefix used to identify lazy objects in settings.

    - `LAZY_INSTANCE_PREFIX: str`
        Prefix used to identify lazy instances in settings.

    Methods:
    - `__init__(self) -> None`
        Initializes the ProjectSettings instance.

    - `__getattr__(self, item: str) -> Any`
        Overrides the attribute getter to dynamically fetch values from registered configurations.

    - `__setattr__(self, key: str, value: Any) -> None`
        Overrides the default `__setattr__` method to handle attribute assignments.
        Sets the specified attribute `key` to the provided value in the `_config_data`.

    - `_get_value_from_config_data(self, item: str) -> Any`
        Retrieves a value from `_config_data`, handling lazy objects and lazy instances.

    - `register_config(self, config: AbstractConfig) -> None`
        Loads and registers config values to the project config

    - `setup_from_environment(self) -> None`
        Sets up PyModuleConfig based on the specified environment variable.
    """

    ENVIRONMENT_VARIABLE: str = "BOT_CONFIG_MODULE"

    LAZY_OBJECT_PREFIX: str = "lazyobj."
    LAZY_INSTANCE_PREFIX: str = "lazyins."

    __slots__ = (
        '_config_data',
    )

    def __init__(self) -> None:
        """
        Initializes the ProjectSettings instance.
        """

        self._config_data: Dict[str, Any] = {}

    def _get_value_from_config_data(self, item: str) -> Any:
        """
        Retrieves a value from `_config_data`

        :param item: `str`
            The attribute name.

        :return: `Any`
            The retrieved value

        :raises:
            :raise KeyError: If `_config_data` has no key `item`
        """

        value = self._config_data[item]

        if isinstance(value, LazyObject):
            return value.obj()
        elif isinstance(value, str) and value.startswith(self.__class__.LAZY_OBJECT_PREFIX):
            lazy_object = LazyObject(".".join(value.split(".")[1:]))
            setattr(self, item, lazy_object)
            return lazy_object.obj()
        # elif isinstance(value, tuple) and (len(value) != 0 and value[0].startswith(self.__class__.LAZY_INSTANCE_PREFIX)):
        #     name, *args = value
        #     lazy_instance = LazyInstance[Any](".".join(name.split(".")[1:]), *args)  # Unavailable
        #     setattr(self, item, lazy_instance)
        #     return lazy_instance.get()

        return value

    def __getattr__(self, item: str) -> Any:
        """
        Overrides the attribute getter to dynamically fetch values from `_config_data`.

        :param item: `str`
            The attribute name.

        :return: `Any`
            The fetched value.

        :raises:
            :raise AttributeError: If the attribute is not found in any of the registered configurations.
        """

        if item.startswith("_"):
            raise AttributeError(f"Cannot get protected attribute '{item}' from project_config")

        try:
            return self._get_value_from_config_data(item)
        except KeyError as error:
            raise AttributeError(f"Project config has no value for key '{item}'") from error

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Overrides the default `__setattr__` method to handle attribute assignments.
        Sets the specified attribute `key` to the provided value in the `_config_data`.

        :param key: `str`
            The attribute name.

        :param value: `Any`
            The value to be assigned to the attribute.
        """
        if key in self.__slots__:
            return super().__setattr__(key, value)

        self._config_data[key] = value

    def register_config(self, config: AbstractConfig) -> None:
        """
        Loads and registers config values to the project config

        :param config: `AbstractConfig`
            The configuration instance.
        """

        self._config_data.update(config.load())

    def setup_from_environment(self) -> None:
        """
        Sets up PyModuleConfig based on the specified environment variable.

        :raises:
            :raise ConfigurationError: If the environment variable is not defined.
        """

        settings_module = os.environ.get(self.__class__.ENVIRONMENT_VARIABLE)

        if not settings_module:
            raise ConfigurationError(
                "Requested settings, but settings are not configured. "
                "You must either define the environment variable %s "
                "or call project_config.set_config() before accessing settings."
                % self.__class__.ENVIRONMENT_VARIABLE
            )

        self.register_config(PyModuleConfig(settings_module))

    def get(self, item: str, default: Optional[Any] = None) -> Any:
        try:
            return getattr(self, item)
        except AttributeError:
            return default


project_settings = ProjectSettings()
