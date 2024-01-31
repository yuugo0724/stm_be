from pynamodb.attributes import UnicodeAttribute
from datetime import datetime, timedelta
from jose import jwt
from core.config import (
  ACCESS_TOKEN_SECRET_KEY,
  ACCESS_TOKEN_EXPIRE_MINUTES,
  REFRESH_TOKEN_SECRET_KEY,
  REFRESH_TOKEN_EXPIRE_DAYS,
  ALGORITHM
)

# プロジェクト内のモジュールをインポート
from models.base_model import BaseModel

class Token(BaseModel):
  username = UnicodeAttribute() # Userモデルのusername
  access_token = UnicodeAttribute()
  refresh_token = UnicodeAttribute(null=True)

  @staticmethod
  def generate_token(username: str, expire: timedelta, secret_key: str):
    expire_at = datetime.utcnow() + expire
    to_encode = {"sub": username, "exp": expire_at}
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm = ALGORITHM)
    return encoded_jwt

  @classmethod
  def create_token(cls, username):
    token = cls()
    token.username = username
    token.access_token = cls.generate_token(
      username = username,
      expire = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES),
      secret_key = ACCESS_TOKEN_SECRET_KEY)
    token.refresh_token = cls.generate_token(
      username = username,
      expire = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
      secret_key = REFRESH_TOKEN_SECRET_KEY)
    return token

  @classmethod
  def refresh_access_token(cls, username):
    token = cls()
    token.username = username
    token.access_token = cls.generate_token(
      username = username,
      expire = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES),
      secret_key = ACCESS_TOKEN_SECRET_KEY)
    return token
