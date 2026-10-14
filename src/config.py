import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///database.db")
    DEBUG: bool = os.getenv("DEBUG", "0") == "1"
    TMDB_BEARER_TOKEN: str = os.getenv("TMDB_BEARER_TOKEN", "token")
    DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "0") == "1"
