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
    
    # External APIs
    OPEN_METEO_URL: str = "https://api.open-meteo.com/v1/forecast"
    TRAFFIC_API_URL: str = "https://mock.traffic.api"
    
    # AI Risk Settings
    RISK_THRESHOLD_HIGH: float = 0.8
    FRAUD_THRESHOLD_HIGH: float = 0.85
    
    class Config:
        env_file = ".env"

settings = Settings()
