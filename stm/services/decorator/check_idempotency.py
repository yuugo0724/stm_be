from functools import wraps

def check_idempotency_by_schema(model_class, key_field, token_field):
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      # 渡されたモデル名を取得
      model_class_name = model_class.__name__.lower()
      # モデル名からスキーマ名を取得
      schema_instance = kwargs.get(model_class_name)
      # スキーマで定義されているkey_field（引数で文字列として渡す）を取得
      hash_key = getattr(schema_instance, key_field, None)
      # スキーマで定義されているtoken_field（引数で文字列として渡す）を取得
      client_request_token = getattr(schema_instance, token_field, None)
      # 冪等性チェック
      existing_item = model_class.get_idempotent_item(hash_key, client_request_token)
      if existing_item is not None:
        return existing_item
      # 元の関数を実行
      return func(*args, **kwargs)
    return wrapper
  return decorator

def check_idempotency_by_key_and_schema(model_class, key_field, token_field):
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      # 渡されたモデル名を取得
      model_class_name = model_class.__name__.lower()
      # モデル名からスキーマ名を取得
      schema_instance = kwargs.get(model_class_name)
      # 引数で指定されたkey_fieldを取得
      hash_key = kwargs.get(key_field)
      # スキーマで定義されているtoken_field（引数で文字列として渡す）を取得
      client_request_token = getattr(schema_instance, token_field, None)
      # 冪等性チェック
      existing_item = model_class.get_idempotent_item(hash_key, client_request_token)
      if existing_item is not None:
        return existing_item
      # 元の関数を実行
      return func(*args, **kwargs)
    return wrapper
  return decorator
