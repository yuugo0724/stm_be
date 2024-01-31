# サードパーティのライブラリをインポート
from datetime import datetime, timezone
from pynamodb.attributes import UTCDateTimeAttribute

class LongDateAttribute(UTCDateTimeAttribute):
  def serialize(self, value):
    # UTC形式に変換
    value = value.astimezone(timezone.utc)
    # YYYY-MM-DD HH:MM:SS形式の文字列に変換して保存（秒まで指定）
    return value.strftime('%Y-%m-%d %H:%M:%S.%f')

  def deserialize(self, value):
    # 文字列からdatetimeオブジェクトに変換
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
