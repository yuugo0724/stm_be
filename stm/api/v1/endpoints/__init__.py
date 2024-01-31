"""
一旦すべてのエンドポイントをまとめる
エンドポイントが増えてきたら機能ごとに分割する
"""

from fastapi import APIRouter
from .user_routers import router as user_router
from .sign_up_routers import router as sign_up_router
from .sign_in_routers import router as sign_in_router
from .token_routers import router as token_router
from .stm_routers import router as stm_router

router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(sign_up_router, prefix="/sign_up", tags=["sign_up"])
router.include_router(sign_in_router, prefix="/sign_in", tags=["sign_in"])
router.include_router(token_router, prefix="/token", tags=["token"])
router.include_router(stm_router, prefix="/stm", tags=["stm"])
