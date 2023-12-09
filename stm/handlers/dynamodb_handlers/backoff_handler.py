import time
from pynamodb.exceptions import PutError
from botocore.exceptions import ClientError
from core.logger_config import logger
from exceptions.dynamodb_exceptions import (
  RetryLimitExceededError,
  ItemAlreadyExistsError
)

def exponential_backoff_handler(operation, max_retries=5, base_delay=1):
  logger.debug("バックオフ処理開始")
  retries = 0
  while retries < max_retries:
    try:
      return operation()
    except PutError as e:
      # PutErrorのcause属性を確認して、それがClientErrorかどうかをチェックします。
      if hasattr(e, 'cause') and isinstance(e.cause, ClientError):
        print(e.cause.response['Error']['Code'])
        error_code = e.cause.response['Error']['Code']
        if error_code == 'ConditionalCheckFailedException':
          logger.debug("書き込みエラー: %s", e)
          raise ItemAlreadyExistsError() from e
      # ログを出力し、リトライ処理を行います。
      logger.error(f"書き込みエラー: {e}")
      if retries >= max_retries - 1:
        raise RetryLimitExceededError() from e
      sleep_time = base_delay * (2 ** retries)
      logger.info(f"リトライ#{retries + 1}: {sleep_time}秒待機...")
      time.sleep(sleep_time)
      retries += 1
    except Exception as e:
      # その他の予期せぬ例外に対しては、エラーログを出力し、例外を再送出します。
      logger.error(f"予期せぬエラー: {e}")
      raise e

# 使用例
# result = exponential_backoff_handler(lambda: some_function_with_possible_put_error())
