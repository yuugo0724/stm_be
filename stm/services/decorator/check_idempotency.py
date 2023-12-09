from functools import wraps

def check_idempotency_by_schema(model_class, schema_name, key_field):
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      print("■テスト: ", model_class)
      print("■テスト: ", args)
      print("■テスト: ", kwargs)
      # モデル名からスキーマ名を取得
      schema_instance = kwargs.get(schema_name)
      # スキーマで定義されているkey_field（引数で文字列として渡す）を取得
      hash_key = getattr(schema_instance, key_field, None)
      # スキーマで定義されているtoken_field（引数で文字列として渡す）を取得
      client_request_token = getattr(schema_instance, 'client_request_token', None)
      # 冪等性チェック
      existing_item = model_class.get_idempotent_item(hash_key, client_request_token)
      if existing_item is not None:
        return existing_item
      # 元の関数を実行
      return func(*args, **kwargs)
    return wrapper
  return decorator

def check_idempotency_by_key_and_schema(model_class, schema_name, key_field):
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      print("■テスト: ", model_class)
      print("■テスト: ", args)
      print("■テスト: ", kwargs)
      # モデル名からスキーマ名を取得
      schema_instance = kwargs.get(schema_name)
      # 引数で指定されたkey_fieldを取得
      print("■テスト: ", key_field)
      hash_key = kwargs.get(key_field)
      print("■テスト: ", hash_key)
      # スキーマで定義されているtoken_field（引数で文字列として渡す）を取得
      client_request_token = getattr(schema_instance, 'client_request_token', None)
      # 冪等性チェック
      existing_item = model_class.get_idempotent_item(hash_key, client_request_token)
      if existing_item is not None:
        return existing_item
      # 元の関数を実行
      return func(*args, **kwargs)
    return wrapper
  return decorator
