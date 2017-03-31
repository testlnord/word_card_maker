import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
API_KEY = os.environ.get("YA_API_KEY")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_USER = os.environ.get("DB_USER")
DB_NAME = os.environ.get("DB_NAME")
SERVER_PORT = int(os.environ.get("SERVER_PORT"))
SECRET_KEY = os.environ.get("SECRET_KEY")
