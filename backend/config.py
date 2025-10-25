import os
from pathlib import Path

# Get the backend directory
BACKEND_DIR = Path(__file__).parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{BACKEND_DIR / 'fleetwise.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False