# 標準ライブラリをインポート
from datetime import datetime
from uuid import UUID

# プロジェクト内のモジュールをインポート
from schemas.stm import (
  StmCreateRequest,
  StmUpdateRequest,
  StmUploadRequest,
  StmDeleteRequest,
  StmBulkDeleteRequest
)
from models.stm import Stm
from handlers.dynamodb_handlers.backoff_handler import exponential_backoff_handler
from handlers.dynamodb_handlers.idempotency_handler import check_idempotency

from core.logger_config import logger

def create_stm(stm: StmCreateRequest, current_user):
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

def upload_stm(records, current_user, client_request_token):
  username = current_user.username
  for record in records:
    try:
      logger.debug("record：%s", record)
      validated_record = StmUploadRequest(**record)
      logger.debug("バリデーション後のrecord：%s", validated_record)
      stm_item = Stm(username = username, client_request_token = client_request_token, **validated_record.model_dump())
      logger.debug("stm_item：%s", stm_item.__dict__)
      exponential_backoff_handler(lambda: stm_item.save())
    except Exception as e:
      logger.error("エラー：%s", e)

def update_stm(stm: StmUpdateRequest, id, current_user):
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

def delete_stm(stm: StmDeleteRequest, id, current_user):
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

def bulk_delete_stm(stm: StmBulkDeleteRequest, current_user):
  username = current_user.username
  deleted_items = []  # 削除されたアイテムを格納するリストを初期化
  for item in stm.items:
    stm_item = Stm.get_filter_item(
      hash_key = item.id,
      username = username,
      version = item.version
    )
    stm_item.deleted_at = datetime.utcnow()
    stm_item.client_request_token = item.client_request_token
    # 冪等性の確保
    # check_idempotency(model = CustomerManage, hash_key = customer_item.id, client_request_token = customer.client_request_token)
    # 指数バックオフでitemを保存
    exponential_backoff_handler(stm_item.save)
    deleted_items.append(stm_item)  # 削除されたアイテムをリストに追加
  return deleted_items