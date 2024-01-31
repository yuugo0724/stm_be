# 標準ライブラリをインポート
from datetime import datetime
from uuid import UUID

# プロジェクト内のモジュールをインポート
from schemas.stm import (
  StmCreate,
  StmUpdate,
  StmDelete
)
from models.stm import Stm
from handlers.dynamodb_handlers.backoff_handler import exponential_backoff_handler
from handlers.dynamodb_handlers.idempotency_handler import check_idempotency

from core.logger_config import logger

def create_stm(stm: StmCreate, current_user):
  username = current_user.username
  schema_data = stm.model_dump()
  logger.debug("schema_data：%s", schema_data)
  stm_item = Stm(username = username, **schema_data)
  logger.debug("customer_item：%s", stm_item.__dict__)
  condition = Stm.id.does_not_exist()
  # 冪等性の確保
  # check_idempotency(model = CustomerManage, hash_key = customer_item.id, client_request_token = customer.client_request_token)
  # 指数バックオフでitemを保存
  exponential_backoff_handler(lambda: stm_item.save(condition))
  return stm_item

def update_stm(stm: StmUpdate, id, current_user):
  username = current_user.username
  stm_item = Stm.get_filter_item(
    hash_key = id,
    username = username,
    version = stm.version
  )
  for key, value in vars(stm).items():
    if value is not None:
      setattr(stm_item, key, value)
  # 冪等性の確保
  # check_idempotency(model = CustomerManage, hash_key = customer_item.id, client_request_token = customer.client_request_token)
  # 指数バックオフでitemを保存
  exponential_backoff_handler(lambda: stm_item.save())
  return stm_item

def delete_stm(stm: StmDelete, id, current_user):
  username = current_user.username
  stm_item = Stm.get_filter_item(
    hash_key = id,
    username = username,
    version = stm.version
  )
  stm_item.deleted_at = datetime.utcnow()
  stm_item.client_request_token = stm.client_request_token
  # 冪等性の確保
  # check_idempotency(model = CustomerManage, hash_key = customer_item.id, client_request_token = customer.client_request_token)
  # 指数バックオフでitemを保存
  exponential_backoff_handler(stm_item.save)
  return stm_item
