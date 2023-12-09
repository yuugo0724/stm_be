# 標準ライブラリをインポート
from datetime import datetime
from uuid import UUID

# プロジェクト内のモジュールをインポート
from schemas.customer_manage import (
  CustomerManageCreate,
  CustomerManageUpdate,
  CustomerManageDelete
)
from models.customer_manage import CustomerManage
from handlers.dynamodb_handlers.backoff_handler import exponential_backoff_handler
from handlers.dynamodb_handlers.idempotency_handler import check_idempotency

from core.logger_config import logger

def create_customer(customer: CustomerManageCreate, current_user):
  username = current_user.username
  schema_data = customer.model_dump()
  logger.debug("schema_data：%s", schema_data)
  customer_item = CustomerManage(username = username, **schema_data)
  logger.debug("customer_item：%s", customer_item.__dict__)
  condition = CustomerManage.id.does_not_exist()
  # 冪等性の確保
  # check_idempotency(model = CustomerManage, hash_key = customer_item.id, client_request_token = customer.client_request_token)
  # 指数バックオフでitemを保存
  exponential_backoff_handler(lambda: customer_item.save(condition))
  return customer_item

def update_customer(customer: CustomerManageUpdate, id, current_user):
  username = current_user.username
  customer_item = CustomerManage.get_filter_item(
    hash_key = id,
    username = username,
    version = customer.version
  )
  for key, value in vars(customer).items():
    if value is not None:
      setattr(customer_item, key, value)
  # 冪等性の確保
  # check_idempotency(model = CustomerManage, hash_key = customer_item.id, client_request_token = customer.client_request_token)
  # 指数バックオフでitemを保存
  exponential_backoff_handler(lambda: customer_item.save())
  return customer_item

def delete_customer(customer: CustomerManageDelete, id, current_user):
  username = current_user.username
  logger.debug("バージョン：%s", customer.version)
  logger.debug("デリーとタイム：%s", datetime.utcnow())
  customer_item = CustomerManage.get_filter_item(
    hash_key = id,
    username = username,
    version = customer.version
  )
  customer_item.deleted_at = datetime.utcnow()
  customer_item.client_request_token = customer.client_request_token
  # 冪等性の確保
  # check_idempotency(model = CustomerManage, hash_key = customer_item.id, client_request_token = customer.client_request_token)
  # 指数バックオフでitemを保存
  exponential_backoff_handler(customer_item.save)
  return customer_item
