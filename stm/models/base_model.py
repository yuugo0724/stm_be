from pynamodb.models import Model
from pynamodb.attributes import UTCDateTimeAttribute
from pynamodb.exceptions import DoesNotExist
from datetime import datetime
# プロジェクト内のモジュールをインポート
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

class ShortDateAttribute(UTCDateTimeAttribute):
  def serialize(self, value):
    # YYYY-MM-DD形式の文字列に変換して保存
    return value.strftime('%Y-%m-%d')

  def deserialize(self, value):
    # 文字列からdatetimeオブジェクトに変換
    return datetime.strptime(value, '%Y-%m-%d')

class LongDateAttribute(UTCDateTimeAttribute):
  def serialize(self, value):
    # YYYY-MM-DD HH:MM:SS形式の文字列に変換して保存（秒まで指定）
    return value.strftime('%Y-%m-%d %H:%M:%S.%f')

  def deserialize(self, value):
    # 文字列からdatetimeオブジェクトに変換
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
