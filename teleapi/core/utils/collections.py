from typing import Optional, Callable, TypeVar, Dict, Any, Iterable

_T = TypeVar("_T")
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class DotDict(Dict[str, Any]):
    """
    A dictionary-like class where attributes are accessed using dot notation.

    Methods:
    - `__init__(self, init_data: Optional[Dict[str, Any]] = None) -> None`
        Initialize DotDict instance

    - `__setattr__(self, key: str, value: Any) -> None`
        Overrides the attribute setter to handle `dict` values by converting them to `DotDict`.

    - `__getattr__(self, item: str) -> Any`
        Overrides the attribute getter to access values using dot notation.

    - `find(self, key: str) -> Any`
        Recursively searches for a key in the DotDict and returns its corresponding value.

    Notes:
    - WARNING: All values that have type `dict` will be replaced with `DotDict`.
    """

    __delattr__ = dict.__delitem__  # type: ignore

    def __init__(self, init_data: Optional[Dict[str, Any]] = None, replace_with_dotdict: bool = True) -> None:
        """
        Initialize DotDict instance

        :param init_data: `Optional[Dict[str, Any]]`
            (Optional) Init data to be added to DotDict.

        Notes:
            WARNING: All values that have type `dict` will be replaced with `DotDict`
        """

        super(DotDict, self).__init__(**(init_data if init_data is not None else {}))

        self._replace_with_dotdict = replace_with_dotdict

        if self._replace_with_dotdict:
            for key, value in self.items():
                if type(value) is dict:
                    setattr(self, key, DotDict(value))

    @property
    def replace_with_dotdict(self) -> bool:
        return self._replace_with_dotdict

    @replace_with_dotdict.setter
    def replace_with_dotdict(self, value: bool) -> None:
        self._replace_with_dotdict = bool(value)

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Overrides the attribute setter to handle `dict` values by converting them to `DotDict`.

        :param key: `str`
            The attribute key.

        :param value: `Any`
            The attribute value.
        """

        if key.startswith("_"):
            self.__dict__[key] = value
            return

        if type(value) is dict and self.replace_with_dotdict:
            dict.__setitem__(self, key, DotDict(value))
        else:
            dict.__setitem__(self, key, value)

    def __getattr__(self, item: str) -> Any:
        """
        Overrides the attribute getter to access values using dot notation.

        :param item: `str`
            The attribute name.

        :return: `Any`
            The attribute value.

        :raises AttributeError: If the attribute is not found.
        """

        try:
            return super(DotDict, self).__getitem__(item)
        except KeyError as error:
            raise AttributeError(f"{self.__class__.__name__} has no attribute '{item}'") from error

    def find(self, key: str) -> Any:
        """
        Recursively searches for a key in the DotDict and returns its corresponding value.

        :param key: `str`
            The key to search for.

        :return: `Any`
            The value corresponding to the key if found, otherwise None.
        """

        return find_in_dict(self, key)


def find_in_dict(dict_: Dict[_KT, _VT], key: _KT) -> Optional[_VT]:
    """
    Recursively searches for a key in a nested dictionary and returns its corresponding value.

    :param dict_: `Dict[_KT, _VT]`
        The dictionary to search.

    :param key: `_KT`
        The key to search for.

    :return: `Optional[_VT]`
        The value corresponding to the key if found, otherwise None.
    """

    if (value := dict_.get(key, None)) is not None:
        return value

    for val in dict_.values():
        if isinstance(val, dict) and (value := find_in_dict(val, key)) is not None:
            return value


def find_in_list(array: Iterable, check: Callable[[Any], bool]) -> Optional[Any]:
    for element in array:
        if check(element):
            return element


def clear_none_values(dictionary: dict) -> dict:
    return {key: value for key, value in dictionary.items() if value is not None}


def replace_substring(original_string: str, start_index: int, end_index: int, replacement_substring: str) -> str:
    if (start_index < 0 or start_index >= len(original_string)) or (end_index < 0 or end_index > len(original_string)) or (start_index > end_index):
        raise IndexError("Invalid start or end index.")

    return original_string[:start_index] + replacement_substring + original_string[end_index:]


def exclude_from_dict(dict_: dict, *exclude) -> dict:
    return {key:value for key, value in dict_.items() if key not in exclude}
