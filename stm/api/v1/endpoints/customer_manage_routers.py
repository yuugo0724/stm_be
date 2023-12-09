# 標準ライブラリをインポート
from typing import List

# サードパーティのライブラリをインポート
from fastapi import APIRouter, Depends

# プロジェクト内のモジュールをインポート
from models.customer_manage import CustomerManage
from schemas.customer_manage import (
  CustomerManageResponse,
  CustomerManageGetResponse,
  CustomerManageCreateResponse,
  CustomerManageUpdateResponse,
  CustomerManageDeleteResponse,
  CustomerManageCreate,
  CustomerManageUpdate,
  CustomerManageDelete
)
from services.customer_manage import customer_manage_service
from core.logger_config import logger
from services.auth_service import get_current_user

router: APIRouter = APIRouter()

@router.get("/{id}", response_model = CustomerManageGetResponse)
def read_customer(id: str, current_user: str = Depends(get_current_user)):
  customer_item = CustomerManage.get_filter_item(hash_key = id, username = current_user.username)
  return customer_item

@router.get("/", response_model = List[CustomerManageGetResponse])
def read_customer_list(current_user: str = Depends(get_current_user)):
  customer_item_list = list(
    CustomerManage.scan(
      (CustomerManage.deleted_at.does_not_exist()) &
      (CustomerManage.username == current_user.username)
    )
  )
  return customer_item_list

@router.post("/", response_model = CustomerManageCreateResponse)
def create_customer(customer: CustomerManageCreate, current_user: str = Depends(get_current_user)):
  logger.debug("リクエスト：%s", customer)
  customer_item = customer_manage_service.create_customer(customer, current_user)
  logger.debug("レスポンス：%s", customer_item.__dict__)
  return customer_item

@router.put("/{id}", response_model = CustomerManageUpdateResponse)
def update_customer(id: str, customer: CustomerManageUpdate, current_user: str = Depends(get_current_user)):
  logger.debug("リクエスト：%s", customer)
  customer_item = customer_manage_service.update_customer(customer, id, current_user)
  logger.debug("レスポンス：%s", customer_item)
  return customer_item

@router.delete("/{id}", response_model = CustomerManageDeleteResponse)
def delete_customer(id: str, customer: CustomerManageDelete, current_user: str = Depends(get_current_user)):
  logger.debug("リクエスト：%s", customer)
  customer_item = customer_manage_service.delete_customer(customer, id, current_user)
  logger.debug("レスポンス：%s", customer_item)
  return customer_item
