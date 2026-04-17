import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_dev_secret")
    JWT_ACCESS_TOKEN_EXPIRES = 3600
