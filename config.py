import os
import json

from dotenv import load_dotenv

load_dotenv()


class Config:
    UPLOAD_DIR = os.getenv("UPLOAD_DIR")
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))
    ALLOW_EXT = set(json.loads(os.getenv("ALLOW_EXT")))
    BASE_URL = os.getenv("BASE_URL")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    SECRET_KEY = os.getenv("SECRET_KEY")
    REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")