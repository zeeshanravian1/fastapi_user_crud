"""
    Core Configuration Module

    Description:
    - This module is responsible for core configuration and read values from
    environment file.

"""

# Importing Python Packages
import secrets
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

# Importing FastAPI Packages

# Importing Project Files

# -----------------------------------------------------------------------------


class CoreConfiguration(BaseSettings):
    """
    Core Settings Class

    Description:
    - This class is used to load core configurations from .env file.

    """

    # Database

    DATABASE: str
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_SCHEMA: str

    # Project Configuration

    CORS_ALLOW_ORIGINS: str
    CORS_ALLOW_METHODS: str
    CORS_ALLOW_HEADERS: str

    PROJECT_TITLE: str = "User Crud APIs Project"
    PROJECT_DESCRIPTION: str = "User Crud APIs Project Documentation"

    VERSION: str = "1.0.0"

    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    # JWT Configuration

    # SECRET_KEY: str
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # SUPER ADMIN CONFIGURATION

    SUPERUSER_USERNAME: str
    SUPERUSER_EMAIL: str
    SUPERUSER_PASSWORD: str
    SUPERUSER_ROLE: str

    # OPENAI

    OPENAI_API_KEY: str
    MODEL_NAME: str = "gpt-3.5-turbo-16k"

    # CoreConfiguration Configuration
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    """
    Test
    """
    return CoreConfiguration()


core_configuration = get_settings()
