from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.user import User
from models.token import Token
from core.config import (
  ACCESS_TOKEN_SECRET_KEY,
  REFRESH_TOKEN_SECRET_KEY,
  ALGORITHM
)
from exceptions.auth_exceptions import (
  AuthenticationException,
  CredentialException
)
from core.logger_config import logger

oauth2_sign_in = OAuth2PasswordBearer(tokenUrl="sign_in")
oauth2_sign_up = OAuth2PasswordBearer(tokenUrl="sign_up")

def authenticate_user_service(username: str, password: str):
  user_item = User.get_item(username)
  if user_item.check_password(plain_password = password, hashed_password = user_item.hashed_password):
    return user_item
  else:
    raise AuthenticationException()

def current_user_service(token: str = Depends(oauth2_sign_in)):
  logger.debug("■current_user_service")
  logger.debug("■token: %s", token)
  try:
    payload = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    logger.debug("■username: %s", username)
    if username is None:
      raise CredentialException()
    user = User.get_item(username)
    if user is None:
      raise AuthenticationException()
    return user
  except JWTError:
    logger.debug("■JWTError: %s", JWTError)
    # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    raise CredentialException()

def refresh_access_token_service(token: str = Depends(oauth2_sign_in)):
  logger.debug("■refresh_access_token_service")
  logger.debug("■token: %s", token)
  try:
    payload = jwt.decode(token, REFRESH_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise AuthenticationException()
    token = Token.refresh_access_token(username)
    return token
  except JWTError:
    raise CredentialException()
