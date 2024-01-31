"""
未実装
いつかやる
"""

from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

# HTTPSを強制するミドルウェア
app.add_middleware(HTTPSRedirectMiddleware)

# 信頼されたホストのみからのリクエストを許可するミドルウェア
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["yourdomain.com", "*.yourdomain.com"])

# 不正なアクセスの検出（例: 繰り返しのログイン失敗）
@app.middleware("http")
async def detect_invalid_access(request: Request, call_next):
    # ここで不正なアクセスの検出ロジックを実装
    # 例: 同じIPからの短時間の間の多数のリクエスト、異常なアクセスパターンなど
    # 不正なアクセスと判断した場合
    # raise HTTPException(status_code=400, detail="Invalid access detected")

    response = await call_next(request)
    return response
