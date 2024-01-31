from fastapi import APIRouter, Depends
# プロジェクト内のモジュールをインポート
from schemas.token import RefreshAccessToken
from services.auth_service import refresh_access_token_service

router: APIRouter = APIRouter()

@router.get("/refresh_access_token", response_model = RefreshAccessToken)
def refresh_token_endpoint(token: str = Depends(refresh_access_token_service)):
  return token
