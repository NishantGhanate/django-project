from rest_framework import status
from rest_framework.exceptions import APIException

from django_project.common import(
    messages as glob_messages
)

class InternalServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = glob_messages.INTERNAL_SERVER_ERROR
    default_code = 'internal_server_error'


class VersionNotSupported(APIException):
    status_code = status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED
    default_detail = glob_messages.VERSION_NOT_SUPPORTED
    default_code = 'version_not_supported'


class ValidationFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = glob_messages.VALIDATION_FAILED
    default_code = 'validation_failed'


class ExpiredSignatureError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = glob_messages.ACCESS_TOKEN_EXPIRED
    default_code = 'expired_signature_error'


class InvalidSignatureError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = glob_messages.TOKEN_INVALID
    default_code = 'invalid_signature_error'


class DecodeError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = glob_messages.DECODE_ERROR
    default_code = 'decode_error'


class InvalidTokenError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = glob_messages.TOKEN_INVALID
    default_code = 'invalid_token_error'