from typing import Dict, Any

from aiohttp import ClientResponse

from teleapi.core.exceptions.teleapi import TeleapiError


class HttpError(TeleapiError):
    default_message = "Unknown HTTP error occurred"


class ApiRequestError(HttpError):
    def __init__(self, message: str = None, response: ClientResponse = None, data: Dict[str, Any] = None) -> None:
        super().__init__(message)

        self.data = data
        self.response = response


class BadRequest(ApiRequestError):
    default_message = "Bad Request"
    description = "Your request could not be understood or was missing required parameters."
    status_code = 400


class Unauthorized(ApiRequestError):
    default_message = "Unauthorized"
    description = "Authentication failed or user lacks necessary permissions."
    status_code = 401


class Forbidden(ApiRequestError):
    default_message = "Forbidden"
    description = "You don't have permission to access the requested resource."
    status_code = 403


class NotFound(ApiRequestError):
    default_message = "Not Found"
    description = "The requested resource could not be found on the server."
    status_code = 404


class MethodNotAllowed(ApiRequestError):
    default_message = "Method Not Allowed"
    description = "The HTTP method used is not allowed for the requested resource."
    status_code = 405


class InternalServerError(ApiRequestError):
    default_message = "Internal Server Error"
    description = "An error occurred on the server, please try again later."
    status_code = 500


class ServiceUnavailable(ApiRequestError):
    default_message = "Service Unavailable"
    description = "The server is temporarily unable to handle the request due to maintenance or overload."
    status_code = 503


class GatewayTimeout(ApiRequestError):
    default_message = "Gateway Timeout"
    description = "The server, while acting as a gateway or proxy, did not receive a timely response."
    status_code = 504


class Conflict(ApiRequestError):
    default_message = "Conflict"
    description = "The request conflicts with the current state of the server's resources."
    status_code = 409


class Gone(ApiRequestError):
    default_message = "Gone"
    description = "The requested resource is no longer available and has been permanently removed."
    status_code = 410


class RequestEntityTooLarge(ApiRequestError):
    default_message = "Request Entity Too Large"
    description = "The requested resource is no longer available and has been permanently removed."
    status_code = 413


class UnsupportedMediaType(ApiRequestError):
    default_message = "Unsupported Media Type"
    description = "The media format of the requested data is not supported."
    status_code = 415


class UnprocessableEntity(ApiRequestError):
    default_message = "Unprocessable Entity"
    description = "The server cannot process the request due to semantic errors."
    status_code = 422


class TooManyRequests(ApiRequestError):
    default_message = "Too Many Requests"
    description = "You have exceeded the rate limit. Please wait before making more requests."
    status_code = 429


class UnknownHttpError(ApiRequestError):
    default_message = "Unknown http error"
    description = "Unknown http error occurred"
    status_code = -1


error_status_mapping = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    405: MethodNotAllowed,
    500: InternalServerError,
    503: ServiceUnavailable,
    504: GatewayTimeout,
    409: Conflict,
    410: Gone,
    413: RequestEntityTooLarge,
    415: UnsupportedMediaType,
    422: UnprocessableEntity,
    429: TooManyRequests
}
