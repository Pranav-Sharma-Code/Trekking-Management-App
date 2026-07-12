import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Base configuration shared by the entire application.
    """
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///trek.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    UPLOAD_FOLDER = "app/static/uploads"
    MAX_CONTENT_LENGTH = 5*1024*1024