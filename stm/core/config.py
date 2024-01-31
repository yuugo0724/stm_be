import os
from dotenv import load_dotenv
import yaml

with open("config.yaml", "r") as yaml_file:
  config = yaml.safe_load(yaml_file)

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
ACCESS_TOKEN_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")
REFRESH_TOKEN_SECRET_KEY = os.getenv("REFRESH_TOKEN_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = config["ACCESS_TOKEN_EXPIRE_MINUTES"]
REFRESH_TOKEN_EXPIRE_DAYS = config["REFRESH_TOKEN_EXPIRE_DAYS"]