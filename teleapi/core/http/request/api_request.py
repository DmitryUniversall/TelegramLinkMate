import json
from abc import ABC, abstractmethod
from typing import Tuple, Any

import aiohttp

from teleapi.core.http.exceptions import UnknownHttpError, error_status_mapping
from teleapi.core.http.request.api_method import APIMethod
from teleapi.core.orm.typing import JsonValue
from teleapi.core.state.settings import project_settings
from teleapi.core.utils.async_tools import async_http_request
from teleapi.core.utils.syntax import default


class AsyncApiRequest(ABC):
    """
    https://core.telegram.org/bots/api#making-requests

    An abstract base class for making asynchronous requests to the Telegram HTTP API.
    """

    def __init__(self, http_method: str, token: str = None) -> None:
        """
        Initialize the AsyncApiRequest instance.

        :param http_method: `str`
            The HTTP method for the API request.
        :param token: `str`
            (Optional) The API token for authorization. If not provided, the class's default API_TOKEN will be used.

        :raises:
            :raise ValueError: If the API token is not specified during initialization.
        """

        self.token = default(token, project_settings.get('API_TOKEN'))

        if self.token is None:
            raise ValueError("Token was not specified")

        self.http_method = http_method
        self.url = self.get_url()

    @property
    @abstractmethod
    def BASE_URL(self) -> str:
        """
        Abstract property to be implemented by subclasses.
        Returns the base URL of the Telegram API.

        :return: `str`
            The base URL.
        """
        ...

    @abstractmethod
    def get_url(self) -> str:
        """
        Abstract method to be implemented by subclasses.
        Constructs and returns the full URL for the API request.

        :return: `str`
            The constructed URL.
        """
        ...

    @abstractmethod
    async def send(self, **kwargs) -> Tuple[aiohttp.ClientResponse, Any]:
        """
        Send the API request asynchronously.

        :param kwargs:
            (Optional) Additional keyword arguments to be passed to the API request.

        :return: `Tuple[aiohttp.ClientResponse, Any]`
            A tuple containing the aiohttp ClientResponse object and the response data.

        :raises:
            :raise ApiRequestError: ApiRequestError or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        """
        ...


class AsyncMethodApiRequest(AsyncApiRequest):
    """
    A subclass of AsyncApiRequest for making asynchronous API requests to the Telegram HTTP API using specific methods.
    """

    BASE_URL: str = "https://api.telegram.org/bot{}/{}"

    def __init__(self, method: APIMethod, *args, **kwargs) -> None:
        """
        Initialize the AsyncMethodApiRequest instance.

        :param method: `APIMethod`
            The specific API method to be called.
        :param args: `tuple`
            Additional positional arguments to be passed to the parent class constructor.
        :param kwargs: `dict`
            Additional keyword arguments to be passed to the parent class constructor.
        """

        self.method = method
        super().__init__(*args, **kwargs)

    def get_url(self) -> str:
        """
        Generate the complete URL for the Telegram API request.

        :return: str
            The complete URL.
        """

        return self.BASE_URL.format(self.token, self.method.value)

    async def send(self, **kwargs) -> Tuple[aiohttp.ClientResponse, JsonValue]:
        """
        Send the Telegram API request asynchronously.

        :param kwargs: `dict`
            Additional keyword arguments to be passed to the API request.

        :return: `Tuple[aiohttp.ClientResponse, JsonValue]`
            A tuple containing the aiohttp ClientResponse object and the JSON response data.

        :raises:
            :raise ApiRequestError: ApiRequestError or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        """

        data = kwargs.get('data')

        if isinstance(data, dict):
            headers = kwargs.get("headers", {})
            headers['Content-Type'] = 'application/json'
            kwargs['headers'] = headers
            kwargs['data'] = json.dumps(data)

        response, bytes_ = await async_http_request(self.http_method, self.url, **kwargs)
        response_data = json.loads(bytes_)

        if not (200 <= response.status <= 299):
            error_type = error_status_mapping.get(response.status, UnknownHttpError)

            raise error_type(
                f"{str(error_type)}: [{self.http_method} -> {self.url}]: {response_data['description']} ({response_data['error_code']})",
                response=response,
                data=response_data
            )

        return response, response_data


class AsyncFileApiRequest(AsyncApiRequest):
    """
    https://core.telegram.org/bots/api#file

    Represents an asynchronous HTTP request for Telegram API file operations.
    """

    BASE_URL: str = "https://api.telegram.org/file/bot{}/{}"

    def __init__(self, file_path: str, *args, **kwargs) -> None:
        """
        Initialize a new instance of AsyncFileApiRequest.

        :param file_path: `str`
            The path to the file in the Telegram API.
        :param args: `tuple`
            Additional positional arguments to pass to the parent constructor.
        :param kwargs: `dict`
            Additional keyword arguments to pass to the parent constructor.
        """

        self.file_path = file_path
        super().__init__(*args, **kwargs)

    def get_url(self) -> str:
        """
        Get the complete URL for the API request.

        :return: `str`
            The complete URL.
        """

        return self.BASE_URL.format(self.token, self.file_path)

    async def send(self, **kwargs) -> Tuple[aiohttp.ClientResponse, bytes]:
        """
        Send the Telegram API request asynchronously.

        :param kwargs: `dict`
            Additional keyword arguments to be passed to the API request.

        :return: `Tuple[aiohttp.ClientResponse, bytes]`
            A tuple containing the aiohttp ClientResponse object and the JSON response data.

        :raises:
            :raise ApiRequestError: ApiRequestError or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        """

        response, bytes_ = await async_http_request(self.http_method, self.url, **kwargs)

        if not (200 <= response.status <= 299):
            response_data = json.loads(bytes_)
            error_type = error_status_mapping.get(response.status, UnknownHttpError)

            raise error_type(
                f"Failed to send request [{self.http_method} -> {self.url}]: {response_data['description']} ({response_data['error_code']})",
                response=response,
                data=response_data
            )

        return response, bytes_


async def method_request(http_method: str,
                         method: APIMethod,
                         token: str = None,
                         **kwargs) -> Tuple[aiohttp.ClientResponse, JsonValue]:
    """
    Send an asynchronous HTTP request for a specific API method. (reduction in interaction with AsyncMethodApiRequest)

    :param http_method: `str`
        The HTTP method to use for the request (e.g., "GET", "POST", "PUT", etc.).

    :param method: `APIMethod`
        The specific API method to request.

    :param token: `str`
        (Optional) The token to be used for authorization. Defaults to `None`.

    :param kwargs: `dict`
        (Optional) Additional keyword arguments to pass to the API request.

    :return: `Tuple[aiohttp.ClientResponse, JsonValue]`
        A tuple containing the HTTP response and the parsed JSON response body.

    :raises:
        :raise ApiRequestError: ApiRequestError or any of its subclasses if the request sent to the Telegram Bot API fails.
        :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
    """

    request = AsyncMethodApiRequest(
        method=method,
        http_method=http_method,
        token=token
    )
    return await request.send(**kwargs)


async def file_request(http_method: str,
                       file_path: str,
                       token: str = None,
                       **kwargs) -> Tuple[aiohttp.ClientResponse, bytes]:
    """
    Sends an HTTP request using the Telegram Bot API to interact with files. (reduction in interaction with AsyncFileApiRequest)

    :param http_method: `str`
        The HTTP method to be used for the request (e.g., 'GET', 'POST', 'PUT', etc.).

    :param file_path: `str`
        The path to the file you want to interact with.

    :param token: `str`
        (Optional) The authentication token for accessing the Telegram Bot API. If not provided, the function will work without authorization.

    :param kwargs: `dict`
        (Optional) Additional keyword arguments that can be passed to the request.

    :return: Tuple[aiohttp.ClientResponse, bytes]
        A tuple containing the HTTP response from the Telegram Bot API and the bytes representing the content of the response.

    :raises:
        :raise ApiRequestError: ApiRequestError or any of its subclasses if the request sent to the Telegram Bot API fails.
        :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
    """

    request = AsyncFileApiRequest(
        file_path=file_path,
        http_method=http_method,
        token=token
    )
    return await request.send(**kwargs)
