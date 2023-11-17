from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from models.error_response import (
  ErrorResponse,
  HttpErrorResponse
)
from core.logger_config import setup_logging

logger = setup_logging()
HANDLERS = []

def register_exception_handler(exception_class):
  def decorator(handler_function):
    HANDLERS.append((exception_class, handler_function))
    return handler_function
  return decorator

def create_exception_response(exc: Exception) -> JSONResponse:
  logger.debug("■Exceptionハンドラー")
  # 予期しないエラーは500のUnexpectedErrorを返す
  status_code = getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
  #error_code = getattr(exc, "error_code", "UnexpectedError")
  error_code = getattr(exc, "error_code", type(exc).__name__)
  details = getattr(exc, "details", "")
  error_message = str(exc)

  logger.debug(status_code)
  logger.error(f"Error Code: {error_code}, Error Message: {error_message}")
  logger.error(f"Error Detail: {details}")

  return JSONResponse(
    status_code=status_code,
    content=ErrorResponse(
      status = status_code,
      error_code = error_code,
      error_message = error_message
    ).model_dump()
  )

def create_http_exception_response(exc: HTTPException) -> JSONResponse:
  logger.debug("■HttpExceptionハンドラー")
  # 予期しないエラーは500のUnexpectedErrorを返す
  status_code = getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
  #error_code = getattr(exc, "error_code", "UnexpectedError")
  error_code = getattr(exc, "error_code", type(exc).__name__)
  details = getattr(exc, "details", "")
  error_message = str(exc)
  headers = getattr(exc, "headers", "")

  logger.debug(status_code)
  logger.error(f"Error Code: {error_code}, Error Message: {error_message}")
  logger.error(f"Error Detail: {details}")

  return JSONResponse(
    content=HttpErrorResponse(
      status = status_code,
      error_code = error_code,
      error_message = error_message,
      headers = headers
    ).model_dump()
  )


