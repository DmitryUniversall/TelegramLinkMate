from typing import TYPE_CHECKING
from teleapi.core.http.request.api_request import method_request
from teleapi.core.http.request.api_method import APIMethod

if TYPE_CHECKING:
    from teleapi.types.user import User


async def get_me() -> 'User':
    """
    Fetches bot user object

    :return: `User`
        Bot user object

    :raises:
        :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
        :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        :raise ValidationError: If the fetched data contains incorrect data or serialization failed
    """

    from teleapi.types.user import UserSerializer

    response, data = await method_request("GET", APIMethod.GET_ME)
    return UserSerializer().serialize(data=data['result'])
