import os
from pathlib import Path

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "AMADOUABDOULGAFAR")
    # Absolute path to the app/ directory (where this file lives)
    APP_DIR = str(Path(__file__).resolve().parent)
