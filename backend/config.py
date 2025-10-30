import os
from pathlib import Path

# Use project root for database
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "backend" / "fleetwise.db"

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False