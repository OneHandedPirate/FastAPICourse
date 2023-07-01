import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_PREFIX = os.getenv('POSTGRES_PREFIX')
SK = os.getenv('SECRET_KEY')
JWT_EXPIRATION_TIME = int(os.getenv('JWT_EXPIRATION_TIME'))
JTW_ALGORITHM = os.getenv('JWT_ALGORITHM')