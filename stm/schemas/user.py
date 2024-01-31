# 標準ライブラリをインポート

# サードパーティのライブラリをインポート
from pydantic import BaseModel

class UserBase(BaseModel):
  username: str
  email: str
  version: int
  client_request_token: str

class SignUpUser(BaseModel):
  username: str
  password: str
  email: str
  client_request_token: str

class UserCreate(BaseModel):
  pass

class UserUpdate(BaseModel):
  email: str
  version: int
  client_request_token: str

class UserDelete(BaseModel):
  version: int
  client_request_token: str

class UserResponse(UserBase):
  pass

class UserGetResponse(UserResponse):
  pass

class UserCreateResponse(UserResponse):
  pass

class UserUpdateResponse(UserResponse):
  pass

class UserDeleteResponse(UserResponse):
  pass
