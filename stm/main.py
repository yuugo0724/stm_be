# サードパーティのライブラリをインポート
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

origins = [
    "http://localhost:3000",  # Next.jsのサーバー
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(debug_router)

# エラーハンドラーの追加
setup_error_handlers(app)

