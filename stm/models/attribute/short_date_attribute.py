# サードパーティのライブラリをインポート
from datetime import datetime
from pynamodb.attributes import UTCDateTimeAttribute

class ShortDateAttribute(UTCDateTimeAttribute):
  def serialize(self, value):
    # UTC形式に変換
    # value = value.astimezone(timezone.utc)
    # YYYY-MM-DD形式の文字列に変換して保存
    return value.strftime('%Y-%m-%d')

  def deserialize(self, value):
    # 文字列からdatetimeオブジェクトに変換
    return datetime.strptime(value, '%Y-%m-%d')
