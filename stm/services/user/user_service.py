# 標準ライブラリをインポート
from datetime import datetime

# プロジェクト内のモジュールをインポート
from schemas.user import (
  UserCreate,
  UserUpdate,
  UserDelete
)
from models.user import User
from handlers.dynamodb_handlers.backoff_handler import exponential_backoff_handler

def create_user(user: UserCreate):
  user_item = User(
    username = user.username,
    email = user.email,
    client_request_token = user.client_request_token
  )
  user_item.password = user.password
  condition = User.username.does_not_exist()
  # 指数バックオフでitemを保存
  exponential_backoff_handler(lambda: user_item.save(condition))
  return user_item

def update_user(username: str, user: UserUpdate):
  user_item = User.get_item(username)
  for key, value in vars(user).items():
    if value is not None:
      setattr(user_item, key, value)
  # 指数バックオフでitemを保存
  exponential_backoff_handler(lambda: user_item.save())
  return user_item

def delete_user(username: str, user: UserDelete):
  user_item = User.get_item(username)
  user_item.deleted_at = datetime.utcnow()
  user_item.client_request_token = user.client_request_token
  # 指数バックオフでitemを保存
  exponential_backoff_handler(user_item.save)
  return user_item
