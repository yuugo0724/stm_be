from pynamodb.models import Model
from pynamodb.exceptions import DoesNotExist

# プロジェクト内のモジュールをインポート
from core.logger_config import logger
from exceptions.dynamodb_exceptions import (
  ItemNotFoundError,
  ItemAlreadyDeletedError,
  VersionMismatchError
)
from core.config import AWS_REGION

class BaseModel(Model):
  class Meta:
    region = AWS_REGION

  @classmethod
  def get_item(cls, hash_key, range_key = None, version = None):
    try:
      item = cls.get(hash_key, range_key=range_key) if range_key else cls.get(hash_key)
      if item.deleted_at is not None:
        raise ItemAlreadyDeletedError
      if version and item.version != version:
        raise VersionMismatchError
    except DoesNotExist:
      raise ItemNotFoundError
    return item

  @classmethod
  def get_any_item(cls, hash_key, range_key = None):
    try:
      item = cls.get(hash_key, range_key = range_key) if range_key else cls.get(hash_key)
    except DoesNotExist:
      item = None
    return item

  @classmethod
  def get_idempotent_item(cls, hash_key, client_request_token):
    """
    操作の再実行による状態の変更がないことを保証する(冪等性)

    Args:
      existing_item: 既に存在する場合そのアイテム、存在しない場合はNone
      client_request_token: オプションのclient_request_token
    Returns:
      None or existing_item: アイテムが存在するかつ、client_request_tokenが一致する場合は取得されたアイテム、それ以外は None
    """
    existing_item = cls.get_any_item(hash_key)
    if existing_item and (not client_request_token or (existing_item.client_request_token == client_request_token)):
      # 既に存在するアイテムをそのまま返す
      logger.debug(f"重複するclient_request_tokenを検出: {client_request_token}。")
      logger.debug("冪等性を保証するため、キャッシュされた結果を返します。")
      return existing_item
    return None
