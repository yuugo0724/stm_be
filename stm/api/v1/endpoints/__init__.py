"""
一旦すべてのエンドポイントをまとめる
エンドポイントが増えてきたら機能ごとに分割する
"""

from fastapi import APIRouter
from .user_routers import router as user_router
from .token_routers import router as token_router

router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(token_router, prefix="/token", tags=["token"])
