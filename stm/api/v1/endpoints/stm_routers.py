# 標準ライブラリをインポート
from typing import List

# サードパーティのライブラリをインポート
from fastapi import APIRouter, Depends

# プロジェクト内のモジュールをインポート
from models.stm import Stm
from schemas.stm import (
  StmResponse,
  StmGetResponse,
  StmCreateResponse,
  StmUpdateResponse,
  StmDeleteResponse,
  StmCreate,
  StmUpdate,
  StmDelete
)
from services.stm import stm_service
from core.logger_config import logger
from services.auth_service import current_user_service

router: APIRouter = APIRouter()

@router.get("/{id}", response_model = StmGetResponse)
def read_stm_endpoint(id: str, current_user: str = Depends(current_user_service)):
  stm_item = Stm.get_filter_item(hash_key = id, username = current_user.username)
  return stm_item

@router.get("/", response_model = List[StmGetResponse])
def read_stm_list_endpoint(current_user: str = Depends(current_user_service)):
  stm_item_list = list(
    Stm.scan(
      (Stm.deleted_at.does_not_exist()) &
      (Stm.username == current_user.username)
    )
  )
  stm_item_list_sorted = sorted(stm_item_list, key=lambda item: item.created_at, reverse=True)
  return stm_item_list_sorted

# @router.get("/", response_model = List[StmGetResponse])
# def read_stm_list(current_user: str = Depends(get_current_user)):
#   stm_item_list = list(
#     Stm.scan(
#       (Stm.deleted_at.does_not_exist()) &
#       (Stm.username == current_user.username)
#     )
#   )
#   return stm_item_list

@router.post("/", response_model = StmCreateResponse)
def create_stm_endpoint(stm: StmCreate, current_user: str = Depends(current_user_service)):
  logger.debug("リクエスト：%s", stm)
  stm_item = stm_service.create_stm(stm, current_user)
  logger.debug("レスポンス：%s", stm_item.__dict__)
  return stm_item

@router.put("/{id}", response_model = StmUpdateResponse)
def update_stm_endpoint(id: str, stm: StmUpdate, current_user: str = Depends(current_user_service)):
  logger.debug("リクエスト：%s", stm)
  stm_item = stm_service.update_stm(stm, id, current_user)
  logger.debug("レスポンス：%s", stm_item)
  return stm_item

@router.delete("/{id}", response_model = StmDeleteResponse)
def delete_stm_endpoint(id: str, stm: StmDelete, current_user: str = Depends(current_user_service)):
  logger.debug("リクエスト：%s", stm)
  stm_item = stm_service.delete_stm(stm, id, current_user)
  logger.debug("レスポンス：%s", stm_item)
  return stm_item
