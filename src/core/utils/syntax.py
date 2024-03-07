import inspect
import warnings
import functools
from typing import Optional, TypeVar

_T = TypeVar("_T")


def default(value: Optional[_T], default_value: _T) -> _T:
    """
    Returns value if value is not None, in other case returns default

    :param value: `Optional[Any]`
        Value to check

    :param default_value: `Any`
        Default value that will be returned if value is None

    :return: `Optional[Any]`
        Returns value if value is not None, in other case returns default

    :raises:
        :raise NoneObjectError: If default value is None
    """

    if default_value is None:
        from src.core.exceptions.generics import NoneObjectError

        raise NoneObjectError("Default value is None")

    return value if value is not None else default_value


def optional_default(value: Optional[_T], default_value: Optional[_T] = None) -> Optional[_T]:
    """
    Returns value if value is not None, in other case returns default

    :param value: `Optional[Any]`
        Value to check

    :param default_value: `Optional[Any]`
        (Optional) Default value, that will be returned if a value is None

    :return: `Optional[Any]`
        Returns value if value is not None, in other case returns default
    """

    return value if value is not None else default_value


def default_any(value: Optional[_T], *defaults) -> _T:
    """
    Returns value if value is not None, in other case returns first not-None default

    :param value: `Optional[T]`
        Initial value

    :param defaults: `tuple`
        Default values

    :return: `T`
        Returns value if value is not None, in other case returns first not-None default

    :raises:
        :raise NoneObjectError: If all default values are None
    """

    if value is not None:
        return value

    for default_value in defaults:
        if default_value is not None:
            return default_value

    from src.core.exceptions.generics import NoneObjectError
    raise NoneObjectError("All default values are None")


def deprecated(reason, warning_format: str = "Called deprecated {kind} {name}: {reason}"):
    """
    Decorator function to mark a function or class as deprecated and issue a warning when it is called.

    :param reason: `Union[str, Type, callable]`
        The reason for deprecation, or a class/function to deprecate.

    :param warning_format: `str`
        The format string for the deprecation warning message.

    :return: `Callable`
        A decorated function or class.

    :raises:
        :raise TypeError: If the provided 'reason' argument is of an unsupported type.
    """

    def decorator(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            name = func.__name__
            kind = 'class' if inspect.isclass(func) else 'function'
            msg = reason if isinstance(reason, str) else f"{kind} is deprecated"

            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(
                message=warning_format.format(kind=kind, name=name, reason=msg),
                category=DeprecationWarning,
                stacklevel=2
            )
            warnings.simplefilter('default', DeprecationWarning)

            return func(*args, **kwargs)

        return new_func

    if isinstance(reason, str):
        return decorator
    elif isinstance(reason, type) or callable(reason):
        return decorator(reason)
    else:
        raise TypeError(repr(type(reason)))
