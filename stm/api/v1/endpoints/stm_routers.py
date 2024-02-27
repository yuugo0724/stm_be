# 標準ライブラリをインポート
from typing import List

# サードパーティのライブラリをインポート
from fastapi import APIRouter, Depends, File, UploadFile, Form
import pandas as pd
from io import StringIO

# プロジェクト内のモジュールをインポート
from models.stm import Stm
from schemas.stm import (
  StmGetResponse,
  StmCreateResponse,
  StmUpdateResponse,
  StmDeleteResponse,
  StmBase,
  StmCreate,
  StmUpdate,
  StmDelete
)
from schemas.schema_mapping import schema_to_dtype
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
  logger.debug("■ソート確認")
  logger.debug([item.__dict__ for item in stm_item_list_sorted])  # 配列の中身を全て展開して表示
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

@router.post("/upload")
async def upload_stm(
    client_request_token: str = Form(...),
    file: UploadFile = File(...),
    current_user: str = Depends(current_user_service
  )):
  # CSVファイルを文字列として読み込む
  content = await file.read()
  string_io = StringIO(content.decode("utf-8"))
  # pandasを使用してCSVを読み込み、DynamoDBに適した形式に変換
  dtype = schema_to_dtype(StmBase)
  logger.debug("dtype：%s", dtype)
  df = pd.read_csv(string_io, dtype=dtype)
  records = df.to_dict(orient="records")
  logger.debug("csvファイルの中身：%s", records)
  stm_service.upload_stm(records, current_user, client_request_token)
  return {"message": "CSVファイルが正常にアップロードされ、DynamoDBにデータが挿入されました。"}

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
