# 標準ライブラリをインポート
from typing import List
import inspect

# サードパーティのライブラリをインポート
from fastapi import APIRouter, Depends

# プロジェクト内のモジュールをインポート
from models.user import User
from schemas.user import (
  UserCreateResponse,
  UserGetResponse,
  UserUpdateResponse,
  UserDeleteResponse,
  SignUpUser,
  UserUpdate,
  UserDelete
)
from services.user import user_service
from core.logger_config import logger
from stm.services.decorator.check_idempotency import (
  check_idempotency_by_schema,
  check_idempotency_by_key_and_schema
)
from services.auth_service import current_user_service

router: APIRouter = APIRouter()

# クライアント用のエンドポイント
@router.get("/", response_model = UserGetResponse)
def current_user_endpoint(current_user: str = Depends(current_user_service)):
  logger.debug("■エンドポイント: %s", inspect.currentframe().f_code.co_name)
  logger.debug("■current_user: %s", current_user.__dict__)
  return current_user

@router.post("/", response_model = UserCreateResponse)
def create_user_endpoint(user: SignUpUser, current_user: str = Depends(current_user_service)):
  logger.debug("■エンドポイント: %s", inspect.currentframe().f_code.co_name)
  logger.debug("■current_user: %s", current_user.__dict__)
  user_item = user_service.create_user(user)
  return user_item

@router.put("/", response_model = UserUpdateResponse)
def update_current_user_endpoint(user: UserUpdate, current_user: str = Depends(current_user_service)):
  logger.debug("■エンドポイント: %s", inspect.currentframe().f_code.co_name)
  logger.debug("■current_user: %s", current_user.__dict__)
  user_item = user_service.update_user(current_user.username, user)
  return user_item

@router.delete("/", response_model = UserDeleteResponse)
def delete_current_user_endpoint(user: UserDelete, current_user: str = Depends(current_user_service)):
  logger.debug("■エンドポイント: %s", inspect.currentframe().f_code.co_name)
  logger.debug("■current_user: %s", current_user.__dict__)
  user_item = user_service.delete_user(current_user.username, user)
  logger.debug("レスポンス：%s", user_item)
  return user_item

# 管理者用のエンドポイント（いつか別のプロジェクトに移行する）
@router.get("/{username}", response_model = UserGetResponse)
def find_user_endpoint(username: str, current_user: str = Depends(current_user_service)):
  logger.debug("■エンドポイント: %s", inspect.currentframe().f_code.co_name)
  logger.debug("username: %s", username)
  logger.debug("■current_user: %s", current_user.__dict__)
  user_item = User.get_item(username)
  return user_item

@router.put("/{username}", response_model = UserUpdateResponse)
def update_user_endpoint(username: str, user: UserUpdate, current_user: str = Depends(current_user_service)):
  logger.debug("■エンドポイント: %s", inspect.currentframe().f_code.co_name)
  logger.debug("■username: %s", username)
  logger.debug("■current_user: %s", current_user.__dict__)
  user_item = user_service.update_user(username, user)
  return user_item

@router.delete("/{username}", response_model = UserDeleteResponse)
def delete_user_endpoint(username: str, user: UserDelete, current_user: str = Depends(current_user_service)):
  logger.debug("■エンドポイント: %s", inspect.currentframe().f_code.co_name)
  logger.debug("■username: %s", username)
  logger.debug("■current_user: %s", current_user.__dict__)
  user_item = user_service.delete_user(username, user)
  logger.debug("レスポンス：%s", user_item)
  return user_item

@router.get("/", response_model = UserGetResponse)
def current_user_endpoint(current_user: str = Depends(current_user_service)):
  logger.debug("■エンドポイント: %s", inspect.currentframe().f_code.co_name)
  logger.debug("■current_user: %s", current_user.__dict__)
  # user_item = User.get_item(current_user.username)
  # return user_item
  return current_user

@router.get("/list", response_model = List[UserGetResponse])
def find_user_list_endpoint(current_user: str = Depends(current_user_service)):
  logger.debug("■エンドポイント: %s", inspect.currentframe().f_code.co_name)
  logger.debug("■current_user: %s", current_user.__dict__)
  user_item_list = list(User.scan(User.deleted_at.does_not_exist()))
  return user_item_list
