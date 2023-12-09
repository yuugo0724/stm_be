# 標準ライブラリをインポート
from typing import List

# サードパーティのライブラリをインポート
from fastapi import APIRouter, Depends

# プロジェクト内のモジュールをインポート
from models.user import User
from schemas.user import (
  UserCreateResponse,
  UserGetResponse,
  UserUpdateResponse,
  UserDeleteResponse,
  UserCreate,
  UserUpdate,
  UserDelete
)
from services.user import user_service
from core.logger_config import logger
from stm.services.decorator.check_idempotency import (
  check_idempotency_by_schema,
  check_idempotency_by_key_and_schema
)
from services.auth_service import get_current_user

router: APIRouter = APIRouter()

@router.get("/{username}", response_model = UserGetResponse)
def read_user(username: str, current_user: str = Depends(get_current_user)):
  user_item = User.get_item(username)
  return user_item

@router.get("/", response_model = List[UserGetResponse])
def read_user_list(current_user: str = Depends(get_current_user)):
  user_item_list = list(User.scan(User.deleted_at.does_not_exist()))
  return user_item_list

@router.post("/", response_model = UserCreateResponse)
def create_user(user: UserCreate, current_user: str = Depends(get_current_user)):
  logger.debug("リクエスト：%s", user)
  user_item = user_service.create_user(user)
  logger.debug("レスポンス：%s", user_item)
  return user_item

@router.post("/signup", response_model = UserCreateResponse)
def signup_user(user: UserCreate):
  logger.debug("リクエスト：%s", user)
  user_item = user_service.create_user(user)
  logger.debug("レスポンス：%s", user_item)
  return user_item

@router.put("/{username}", response_model = UserUpdateResponse)
def update_user(username: str, user: UserUpdate, current_user: str = Depends(get_current_user)):
  logger.debug("リクエスト：%s", user)
  user_item = user_service.update_user(username, user)
  logger.debug("レスポンス：%s", user_item)
  return user_item

@router.delete("/{username}", response_model = UserDeleteResponse)
def delete_user(username: str, user: UserDelete, current_user: str = Depends(get_current_user)):
  logger.debug("リクエスト：%s", user)
  user_item = user_service.delete_user(username, user)
  logger.debug("レスポンス：%s", user_item)
  return user_item
