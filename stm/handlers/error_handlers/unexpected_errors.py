from fastapi import Request
from .common import (
  register_exception_handler,
  create_exception_response
)

# 予期しないエラー
@register_exception_handler(Exception)  # デコレータを適用
async def unexpected_exception_handler(request: Request, exc: Exception):
  return create_exception_response(exc)
