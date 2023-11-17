from fastapi import status

class BaseException(Exception):
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

class ItemNotFoundError(BaseException):
  """
  アイテムが存在しないときに発生する
  """
  message = "アイテムが存在しません。"
  status_code = status.HTTP_400_BAD_REQUEST

class ItemAlreadyDeletedError(BaseException):
  """
  アイテムが削除済みのときに発生する
  """
  message = "削除済みのアイテムです。"
  status_code = status.HTTP_400_BAD_REQUEST

class VersionMismatchError(BaseException):
  """
  楽観的ロックによるバージョン不一致だった場合に発生する
  """
  message = "バージョンが不一致です。"
  status_code = status.HTTP_400_BAD_REQUEST

class RetryLimitExceededError(BaseException):
  """
  バックオフによるすべての再試行が失敗した場合に発生する
  """
  message = "全ての再試行に失敗しました。"
  status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

class ItemAlreadyExistsError(BaseException):
  """
  重複したデータを作成しようとした場合に発生する
  """
  message = "データが重複しています。"
  status_code = status.HTTP_400_BAD_REQUEST
