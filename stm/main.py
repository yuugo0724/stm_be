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
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",  # Next.jsのサーバー
]

# ミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost:3000", "127.0.0.1:3000", "localhost", "127.0.0.1"])
# app.add_middleware(HTTPSRedirectMiddleware)

app.include_router(router)
app.include_router(debug_router)

# エラーハンドラーの追加
setup_error_handlers(app)

