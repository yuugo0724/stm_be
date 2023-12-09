# PydanticのValidationErrorはFastAPIのRequestValidationErrorに変換されて送出される
from fastapi.exceptions import RequestValidationError
from .common import (
  register_exception_handler,
  create_exception_response
)

@register_exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
  return create_exception_response(exc)
