# サードパーティのライブラリをインポート
from pynamodb.models import Model
from pynamodb.exceptions import DoesNotExist
from datetime import datetime, timezone
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, VersionAttribute, UTCDateTimeAttribute, BooleanAttribute, Attribute
from pynamodb_attributes import UUIDAttribute

# プロジェクト内のモジュールをインポート
from models.attribute.short_date_attribute import ShortDateAttribute
from models.attribute.long_date_attribute import LongDateAttribute
from core.logger_config import logger
from exceptions.dynamodb_exceptions import (
  ItemNotFoundError,
  ItemAlreadyDeletedError,
  VersionMismatchError
)

from core.logger_config import logger

from core.config import AWS_REGION

class BaseModel(Model):
  class Meta:
    region = AWS_REGION

  version = VersionAttribute()
  client_request_token = UnicodeAttribute(default = None, null=True)  # 必要に応じてnullを設定
  # deleted_atの扱いを変更。nullを許容し、実際に削除が行われたときにタイムスタンプを設定
  deleted_at = LongDateAttribute(default = None, null=True)
  created_at = LongDateAttribute(default = lambda: datetime.now())
  updated_at = LongDateAttribute(default = lambda: datetime.now())

  def save(self, condition=None, **expected_values):
    # 保存操作のたびにupdated_atを更新
    self.updated_at = datetime.now(timezone.utc)
    super(BaseModel, self).save(condition=condition, **expected_values)

  @classmethod
  def get_item(cls, hash_key, range_key = None, version = None):
    try:
      item = cls.get(hash_key, range_key=range_key) if range_key else cls.get(hash_key)
      if item.deleted_at is not None:
        raise ItemAlreadyDeletedError()
      if version and item.version != version:
        raise VersionMismatchError()
    except DoesNotExist:
      raise ItemNotFoundError()
    return item

  @classmethod
  def get_filter_item(cls, hash_key, range_key = None, version = None, **filters):
    try:
      # 既存のget_itemメソッドを使用してアイテムを取得
      item = cls.get_item(hash_key = hash_key, range_key = range_key, version = version)
      # 追加のフィルタを適用
      for key, value in filters.items():
        if not hasattr(item, key) or getattr(item, key) != value:
          raise ItemNotFoundError(f"Item with {key}={value} not found.")
    except DoesNotExist:
      raise ItemNotFoundError()
    return item

  @classmethod
  def get_any_item(cls, hash_key, range_key = None):
    try:
      item = cls.get(hash_key, range_key = range_key) if range_key else cls.get(hash_key)
    except DoesNotExist:
      item = None
    return item

  @classmethod
  def convert_to_iso8601(cls, date):
    return datetime.isoformat(date)
