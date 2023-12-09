# 標準ライブラリをインポート

# サードパーティのライブラリをインポート
from fastapi import APIRouter

# プロジェクト内のモジュールをインポート
from core.logger_config import setup_logging
from handlers.error_handlers.common import HANDLERS
from core.logger_config import setup_logging
from pydantic import BaseModel, Field, validator
from datetime import datetime

class DebugCustomer(BaseModel):
  application_date: datetime = Field(..., title="申込日")
  class Config:
    json_encoders = {
      datetime: lambda dt: dt.isoformat()
    }
  # @validator('application_date', pre=True)
  # def parse_application_date(cls, value):
  #   try:
  #     # 文字列をISO 8601形式の日付に変換
  #     return datetime.fromisoformat(value)
  #   except ValueError:
  #     # 有効なISO 8601形式の日付でない場合は例外を発生させる
  #     raise ValueError(f"Invalid date format for application_date: {value}")

router = APIRouter()
logger = setup_logging()

@router.get("/HANDLERS")
def debug_HANDLERS():
  logger.debug("■デバッグ")
  return {"handlers": str(HANDLERS)}

@router.post("/datetime", response_model = DebugCustomer)
def debug_datetime(customer_item: DebugCustomer):
  logger.debug("■デバッグ")
  return {"datetime": customer_item.application_date}
