import json
from typing import Any, Dict
from aiohttp import FormData


def prepare_field(value: Any) -> str:
    """
    Converts specified value to str for it to be added to FormData

    :param value: `Any`
        Value to be converted

    :return: `str`
        Converted value
    """

    try:
        return value if isinstance(value, (str, bytes)) else json.dumps(value)
    except Exception as error:
        raise ValueError(f"Unable to serialize {value}") from error


def prepare_data(data: Dict[Any, Any]) -> Dict[str, str]:
    """
    Converts all fields of data to str for it to be added to FormData

    :param data: `dict`
        Dict with data to be converted

    :return: `dict`
        Dict with converted data
    """

    return {str(key): prepare_field(value) for key, value in data.items()}


def make_form_data(data: Dict[str, Any], form_data: FormData = None) -> FormData:
    """
    Makes `FormData` from specified data dict. Adds field from `data` to `form_data` if it specified, else creates new

    :param data: `dict`
        Dict with data to be converted

    :param form_data: `FormData`
        `FormData` object where to add fields

    :return: `FormData`
        `FormData` object with added fields
    """

    if form_data is None:
        form_data = FormData()

    for name, value in data.items():
        form_data.add_field(name, prepare_field(value))

    return form_data
