# 標準ライブラリをインポート
import bcrypt

# サードパーティのライブラリをインポート
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, VersionAttribute, UTCDateTimeAttribute, BooleanAttribute, Attribute
from pynamodb_attributes import UUIDAttribute

# プロジェクト内のモジュールをインポート
from models.base_model import BaseModel, ShortDateAttribute, LongDateAttribute

class User(BaseModel):
  class Meta(BaseModel.Meta):
    table_name = 'users'

  @property
  def password(self):
    return self.__password

  @password.setter
  def password(self, plaintext_password):
    # ハッシュ化の処理
    hashed = self.get_hashed_password(plaintext_password)
    self.__password = hashed
    self.hashed_password = hashed

  def get_hashed_password(self, plain_password):
    # plain_passwordをbcryptでソルトを用いてハッシュ化する
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

  def check_password(self, plain_password, hashed_password):
    # ハッシュとplain_passwordを照合
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

  # hash_key（パーティションキー）
  # range_key（ソートキー）※今回はなし
  # lambdaでdefaultを設定しないと、Userクラスがインポートされたときにのみuuid4()が実行されるため、同じidが設定されてしまう
  # id = UUIDAsStringAttribute(hash_key= True, default = lambda: str(uuid4()))
  username = UnicodeAttribute(hash_key = True)
  # DynamoDBではTEXT型はないため、UnicodeAttributeを使用
  # schemaではpasswordを受け取り、modelではhashed_passwordを保存する
  hashed_password = UnicodeAttribute()
  email = UnicodeAttribute()
  version = VersionAttribute()
  client_request_token = UnicodeAttribute(default = None, null=True)  # 必要に応じてnullを設定
  # deleted_atの扱いを変更。nullを許容し、実際に削除が行われたときにタイムスタンプを設定
  deleted_at = LongDateAttribute(default = None, null=True)
