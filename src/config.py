from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dasdafg473f347f4378d237g2g783d")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
    DEBUG = os.getenv("DEBUG", "0") == "1"
