
from uuid import uuid4

# サードパーティのライブラリをインポート
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
    BooleanAttribute,
    VersionAttribute
)
from pynamodb_attributes import UUIDAttribute

# プロジェクト内のモジュールをインポート
from models.base_model import BaseModel, ShortDateAttribute, LongDateAttribute

class Stm(BaseModel):
  class Meta(BaseModel.Meta):
    table_name = 'stm'
  # lambdaでdefaultを設定しないと、クラスがインポートされたときにのみuuid4()が実行されるため、同じidが設定されてしまう
  id = UnicodeAttribute(hash_key= True, default = lambda: str(uuid4()))
  username = UnicodeAttribute()
  # 住所
  address = UnicodeAttribute()
  # 年齢
  age = NumberAttribute()
  # 年収
  annual_income = NumberAttribute()
  # AP
  annual_premium = NumberAttribute()
  # AC
  annualized_premium_equivalent = NumberAttribute()
  # 申込日
  application_date = ShortDateAttribute()
  # 連絡先
  contact_information = UnicodeAttribute()
  # 契約完了日
  contract_completion_date = ShortDateAttribute()
  # 契約種別
  contract_type = UnicodeAttribute()
  # 生年月日
  date_of_birth = ShortDateAttribute()
  # 初回面談日
  first_interview_date = ShortDateAttribute()
  # 苗字
  last_name = UnicodeAttribute()
  # 名前
  first_name = UnicodeAttribute()
  # 苗字フリガナ
  last_name_kana = UnicodeAttribute()
  # 名前
  first_name_kana = UnicodeAttribute()
  # 性別
  gender = UnicodeAttribute()
  # 世帯
  household = UnicodeAttribute()
  # 保険期間終了日
  insurance_policy_end_date = ShortDateAttribute()
  # 保険期間開始日
  insurance_policy_start_date = ShortDateAttribute()
  # 保険料
  insurance_premium = NumberAttribute()
  # 保険種目
  insurance_type = UnicodeAttribute()
  # 訪問回数
  number_of_visits = NumberAttribute()
  # 支払方法
  payment_method = UnicodeAttribute()
  # 郵便番号
  postal_code = UnicodeAttribute()
  # 証券番号
  security_number = UnicodeAttribute()
  # ステータス
  status = UnicodeAttribute()
  # 終身保険フラグ
  whole_life_insurance_flag = BooleanAttribute()
