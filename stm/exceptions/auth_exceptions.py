from fastapi import HTTPException, status

class BaseException(HTTPException):
  """
  基本的なエラーの基底例外
  """
  message: str
  status_code: int

  def __init__(self, details: str = None):
    self.details = details

  # error_codeにクラス名を入れるプロパティ
  @property
  def error_code(self) -> str:
    return self.__class__.__name__
  # インスタンスを文字列変換した際にmessageを出力するプロパティ
  def __str__(self) -> str:
    return self.message

class AuthenticationException(BaseException):
  """
  認証ユーザが存在しないときに発生する
  """
  message = "認証に失敗しました。"
  status_code = status.HTTP_401_UNAUTHORIZED
  headers = {"WWW-Authenticate": "Bearer"}

class CredentialException(BaseException):
  """
  認証情報が無効なときに発生する
  """
  message = "認証情報が無効です。"
  status_code = status.HTTP_401_UNAUTHORIZED
  headers = {"WWW-Authenticate": "Bearer"}
