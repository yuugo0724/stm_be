from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from models.user import User
from core.config import (
  JWT_SECRET_KEY,
  ALGORITHM
)
from stm.exceptions.auth_exceptions import (
  AuthenticationException,
  CredentialException
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(username: str, password: str):
  user_item = User.get_item(username)
  if user_item.check_password(plain_password = password, hashed_password = user_item.hashed_password):
    return user_item
  else:
    raise AuthenticationException()

def create_access_token(data: dict, expires_delta: timedelta = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes = 15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm = ALGORITHM)
  return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
  try:
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise CredentialException()
    user = User.get_item(username)
    if user is None:
      raise CredentialException()
    return user
  except JWTError:
    raise CredentialException()
