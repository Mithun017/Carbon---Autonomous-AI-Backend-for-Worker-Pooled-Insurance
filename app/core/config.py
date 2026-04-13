from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Carbon Backend"
    SECRET_KEY: str = "development-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    DATABASE_URL: str = "sqlite:///./carbon.db"
    MOCK_OTP: bool = True
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
