# 標準ライブラリをインポート
import bcrypt
from datetime import datetime

# サードパーティのライブラリをインポート
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, VersionAttribute, UTCDateTimeAttribute, BooleanAttribute, Attribute
from pynamodb_attributes import UUIDAttribute
from passlib.hash import pbkdf2_sha256  # bcryptからpasslibへ変更

# プロジェクト内のモジュールをインポート
from models.attribute.short_date_attribute import ShortDateAttribute
from models.attribute.long_date_attribute import LongDateAttribute
from models.base_model import BaseModel

class User(BaseModel):
  class Meta(BaseModel.Meta):
    table_name = 'users'

  @property
  def password(self):
    return self.__password

  @password.setter
  def password(self, plaintext_password):
    # ハッシュ化の処理をpasslibで行う
    hashed = self.get_hashed_password(plaintext_password)
    self.__password = hashed
    self.hashed_password = hashed

  def get_hashed_password(self, plain_password):
    # plain_passwordをpbkdf2_sha256でハッシュ化する
    hashed = pbkdf2_sha256.hash(plain_password)
    return hashed

  def check_password(self, plain_password, hashed_password):
    # ハッシュとplain_passwordを照合
    return pbkdf2_sha256.verify(plain_password, hashed_password)

  # hash_key（パーティションキー）
  # range_key（ソートキー）※今回はなし
  # lambdaでdefaultを設定しないと、Userクラスがインポートされたときにのみuuid4()が実行されるため、同じidが設定されてしまう
  # id = UUIDAsStringAttribute(hash_key= True, default = lambda: str(uuid4()))
  username = UnicodeAttribute(hash_key = True)
  # DynamoDBではTEXT型はないため、UnicodeAttributeを使用
  # schemaではpasswordを受け取り、modelではhashed_passwordを保存する
  hashed_password = UnicodeAttribute()
  email = UnicodeAttribute()
  # version = VersionAttribute()
  # client_request_token = UnicodeAttribute(default = None, null=True)  # 必要に応じてnullを設定
  # # deleted_atの扱いを変更。nullを許容し、実際に削除が行われたときにタイムスタンプを設定
  # deleted_at = LongDateAttribute(default = None, null=True)
  # created_at = LongDateAttribute(default = lambda: datetime.now())
