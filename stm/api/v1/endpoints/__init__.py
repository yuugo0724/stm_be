"""
一旦すべてのエンドポイントをまとめる
エンドポイントが増えてきたら機能ごとに分割する
"""

from fastapi import APIRouter
from .user_routers import router as user_router
from .login_routers import router as login_router
from .customer_manage_routers import router as customer_manage_router

router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(login_router, prefix="/login", tags=["login"])
router.include_router(customer_manage_router, prefix="/stm", tags=["stm"])
