import os
from datetime import timedelta

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - dependency fallback
    load_dotenv = None


if load_dotenv:
    load_dotenv()


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Application configuration loaded by the app factory."""

    SECRET_KEY = os.getenv("SECRET_KEY", "secretkey")
    DATABASE = os.getenv("DATABASE_PATH", os.path.join(BASE_DIR, "study.db"))
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "5000"))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "0") == "1"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)
