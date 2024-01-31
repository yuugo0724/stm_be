from fastapi import APIRouter
# プロジェクト内のモジュールをインポート
from services.user import user_service
from models.token import Token
from schemas.token import CreateToken
from schemas.user import SignUpUser

router: APIRouter = APIRouter()

@router.post("/", response_model = CreateToken)
def sign_up_endpoint(user: SignUpUser):
  user_item = user_service.create_user(user)
  token = Token.create_token(user_item.username)
  return token
