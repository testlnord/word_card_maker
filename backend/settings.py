import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
API_KEY = os.environ.get("YA_API_KEY")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_USER = os.environ.get("DB_USER")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
SERVER_PORT = int(os.environ.get("SERVER_PORT"))
SERVER_HOST = os.environ.get("SERVER_HOST")
SECRET_KEY = os.environ.get("SECRET_KEY")
