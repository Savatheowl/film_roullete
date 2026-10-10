import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
    DEBUG = os.getenv("DEBUG", "0") == "1"
