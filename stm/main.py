# サードパーティのライブラリをインポート
from fastapi import FastAPI

# プロジェクト内のモジュールをインポート
from api.v1.endpoints import router
from api.debug.endpoints import debug_router
from core.error_config import setup_error_handlers
from handlers.error_handlers import (
  dynamodb_errors,
  pydantic_errors,
  unexpected_errors,
  auth_errors
)

app = FastAPI()
app.include_router(router)
app.include_router(debug_router)

# エラーハンドラーの追加
setup_error_handlers(app)

