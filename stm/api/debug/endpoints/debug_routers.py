# 標準ライブラリをインポート

# サードパーティのライブラリをインポート
from fastapi import APIRouter

# プロジェクト内のモジュールをインポート
from core.logger_config import setup_logging
from handlers.error_handlers.common import HANDLERS
from core.logger_config import setup_logging



router = APIRouter()
logger = setup_logging()

@router.get("/HANDLERS")
def debug_HANDLERS():
  logger.debug("■デバッグ")
  return {"handlers": str(HANDLERS)}

