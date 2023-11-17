"""
一旦すべてのエンドポイントをまとめる
エンドポイントが増えてきたら機能ごとに分割する
"""

from fastapi import APIRouter
from .debug_routers import router as debug_router

router = APIRouter()

router.include_router(debug_router, prefix="/debug", tags=["debug"])
