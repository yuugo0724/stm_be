# 標準ライブラリをインポート
from datetime import datetime
# サードパーティのライブラリをインポート
from pydantic import BaseModel

class CreateToken(BaseModel):
  access_token: str
  refresh_token: str

class RefreshAccessToken(BaseModel):
  access_token: str
