from starlette.responses import JSONResponse
from core.logger_config import logger

def check_idempotency(model, hash_key, client_request_token):
  # 冪等性チェック
  """
  操作の再実行による状態の変更がないことを保証する(冪等性)
  Args:
    existing_item: 既に存在する場合そのアイテム、存在しない場合はNone
    client_request_token: オプションのclient_request_token
  Returns:
    None or existing_item: アイテムが存在するかつ、client_request_tokenが一致する場合は取得されたアイテム、それ以外は None
  """
  print("■model：",model)
  print("■hash_key：",hash_key)
  print("■client_request_token：",client_request_token)
  existing_item = model.get_any_item(hash_key)
  if existing_item and (not client_request_token or (existing_item.client_request_token == client_request_token)):
    # 既に存在するアイテムをそのまま返す
    logger.debug(f"重複するclient_request_tokenを検出: {client_request_token}。")
    logger.debug("冪等性を保証するため、キャッシュされた結果を返します。")
    #return existing_item
    print("■冪等性の確認：",existing_item)
    return JSONResponse(content=existing_item, status_code = 200)
