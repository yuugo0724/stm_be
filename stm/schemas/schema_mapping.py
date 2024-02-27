from pydantic import BaseModel
from datetime import datetime
from core.logger_config import logger

# StmUploadスキーマからdtype用の辞書を生成する関数
def schema_to_type(schema: BaseModel) -> dict:
  dtype_map = {}
  logger.debug("スキーママッピング：%s", schema.__annotations__)
  for field_name, field_type in schema.__annotations__.items():
    logger.debug("フィールド情報：%s %s", field_name, field_type)
    if field_type == int:
      dtype_map[field_name] = int
    elif field_type == float:
      dtype_map[field_name] = float
    elif field_type == str:
      dtype_map[field_name] = str
    elif field_type == datetime.date:
      dtype_map[field_name] = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date()
    # 他のデータ型に対する処理...
  return dtype_map
