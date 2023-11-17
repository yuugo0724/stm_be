# サードパーティのライブラリをインポート
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
# プロジェクト内のモジュールをインポート
from models.token import Token
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from services.auth_service import (
  authenticate_user,
  create_access_token
)

router: APIRouter = APIRouter()

@router.post("/", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
  user_item = authenticate_user(form_data.username, form_data.password)
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
    data = {"sub": user_item.username}, expires_delta = access_token_expires
  )
  return {"access_token": access_token, "token_type": "bearer"}
