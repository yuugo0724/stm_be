from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
# プロジェクト内のモジュールをインポート
from models.token import Token
from schemas.token import CreateToken
from services.auth_service import authenticate_user_service

router: APIRouter = APIRouter()

@router.post("/", response_model = CreateToken)
def sign_in_endpoint(form_data: OAuth2PasswordRequestForm = Depends()):
  user_item = authenticate_user_service(form_data.username, form_data.password)
  token = Token.create_token(user_item.username)
  return token
