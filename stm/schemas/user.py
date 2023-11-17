# 標準ライブラリをインポート

# サードパーティのライブラリをインポート
from pydantic import BaseModel

class UserBase(BaseModel):
  client_request_token: str

class UserCreate(UserBase):
  username: str
  email: str
  password: str

class UserUpdate(UserBase):
  email: str
  version: int

class UserDelete(UserBase):
  version: int

class UserResponse(UserBase):
  username: str
  email: str
  version: int

class UserGetResponse(UserResponse):
  pass

class UserCreateResponse(UserResponse):
  pass

class UserUpdateResponse(UserResponse):
  pass

class UserDeleteResponse(UserResponse):
  pass
