from fastapi import Request
from exceptions.dynamodb_exceptions import (
  ItemNotFoundError,
  ItemAlreadyDeletedError,
  VersionMismatchError,
  RetryLimitExceededError,
  ItemAlreadyExistsError
)
from .common import (
  register_exception_handler,
  create_exception_response
)

### dynamodbのトランザクション関連
@register_exception_handler(ItemNotFoundError)  # デコレータを適用
async def item_not_found_error_handler(request: Request, exc: ItemNotFoundError):
  return create_exception_response(exc)

@register_exception_handler(ItemAlreadyDeletedError)  # デコレータを適用
async def item_already_deleted_error_handler(request: Request, exc: ItemAlreadyDeletedError):
  return create_exception_response(exc)

@register_exception_handler(VersionMismatchError)  # デコレータを適用
async def version_mismatch_error_handler(request: Request, exc: VersionMismatchError):
  return create_exception_response(exc)

@register_exception_handler(RetryLimitExceededError)  # デコレータを適用
async def retry_limit_exceeded_error_handler(request: Request, exc: RetryLimitExceededError):
  return create_exception_response(exc)

@register_exception_handler(ItemAlreadyExistsError)  # デコレータを適用
async def item_already_exists_error_handler(request: Request, exc: ItemAlreadyExistsError):
  return create_exception_response(exc)
