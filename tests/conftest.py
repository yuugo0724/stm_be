import pytest
from moto import mock_dynamodb2
from stm.models.user import User  # あなたのモデルをインポート

@pytest.fixture(scope="function")
def dynamodb():
  with mock_dynamodb2():
    yield

@pytest.fixture(scope="function")
def create_tables(dynamodb):
  User.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
  yield
  User.delete_table()
