# PydanticのValidationErrorはFastAPIのRequestValidationErrorに変換されて送出される
from stm.exceptions.auth_exceptions import (
  AuthenticationException,
  CredentialException
)
from .common import (
  register_exception_handler,
  create_exception_response,
  create_http_exception_response
)

@register_exception_handler(AuthenticationException)
async def authentication_error_handler(request, exc: AuthenticationException):
  return create_http_exception_response(exc)

@register_exception_handler(CredentialException)
async def credential_exception_handler(request, exc: CredentialException):
  return create_http_exception_response(exc)
