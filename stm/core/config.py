import os
from dotenv import load_dotenv
import yaml

with open("config.yaml", "r") as yaml_file:
  config = yaml.safe_load(yaml_file)

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = config["ACCESS_TOKEN_EXPIRE_MINUTES"]
