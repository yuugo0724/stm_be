# 標準ライブラリをインポート
from datetime import date
# サードパーティのライブラリをインポート
from pydantic import BaseModel, Field
from core.logger_config import logger

class StmBase(BaseModel):
  address: str = Field(..., description="住所")
  age: int = Field(..., description="年齢")
  annual_income: int = Field(..., description="年収")
  annual_premium: int = Field(..., description="AP")
  annualized_premium_equivalent: int = Field(..., description="AC")
  application_date: date = Field(..., description="申込日")
  contact_information: str = Field(..., description="連絡先")
  contract_completion_date: date = Field(..., description="契約完了日")
  contract_type: str = Field(..., description="契約種別")
  date_of_birth: date = Field(..., description="生年月日")
  first_interview_date: date = Field(..., description="初回面談日")
  last_name: str = Field(..., description="苗字")
  first_name: str = Field(..., description="名前")
  last_name_kana: str = Field(..., description="苗字フリガナ")
  first_name_kana: str = Field(..., description="名前フリガナ")
  gender: str = Field(..., description="性別")
  household: str = Field(..., description="世帯")
  insurance_policy_end_date: date = Field(..., description="保険期間終了日")
  insurance_policy_start_date: date = Field(..., description="保険期間開始日")
  insurance_premium: int = Field(..., description="保険料")
  insurance_type: str = Field(..., description="保険種目")
  number_of_visits: int = Field(..., description="訪問回数")
  payment_method: str = Field(..., description="支払方法")
  postal_code: str = Field(..., description="郵便番号")
  security_number: str = Field(..., description="証券番号")
  status: str = Field(..., description="ステータス")
  whole_life_insurance_flag: bool = Field(..., description="終身保険フラグ")

class StmCreate(StmBase):
  client_request_token: str = Field(..., description="クライアントリクエストトークン")

class StmUpload(StmBase):
  pass

class StmUpdate(StmBase):
  version: int = Field(..., description="バージョン")
  client_request_token: str = Field(..., description="クライアントリクエストトークン")

class StmDelete(BaseModel):
  version: int = Field(..., description="バージョン")
  client_request_token: str = Field(..., description="クライアントリクエストトークン")

class StmResponse(StmBase):
  id: str = Field(..., description="ID")
  username: str = Field(..., description="ユーザー名")
  version: int = Field(..., description="バージョン")
  client_request_token: str = Field(..., description="クライアントリクエストトークン")

class StmGetResponse(StmResponse):
  pass

class StmCreateResponse(StmResponse):
  pass

class StmUpdateResponse(StmResponse):
  pass

class StmDeleteResponse(StmResponse):
  pass
