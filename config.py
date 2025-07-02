import os
import json

from dotenv import load_dotenv

load_dotenv()


class Config:
    UPLOAD_DIR = os.getenv("UPLOAD_DIR")
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))
    ALLOW_EXT = set(json.loads(os.getenv("ALLOW_EXT")))
    BASE_URL = os.getenv("BASE_URL")
