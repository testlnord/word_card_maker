import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
API_KEY = os.environ.get("YA_API_KEY")
