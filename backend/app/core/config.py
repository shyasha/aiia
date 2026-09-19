import json
from typing import List

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AIIA Study Workspace API"
    VERSION: str = "0.1.0-demo"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite+aiosqlite:///./aiia_ctms.db"
    DATABASE_URL_SYNC: str = "sqlite:///./aiia_ctms.db"

    SECRET_KEY: str = "change-this-development-secret-before-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1
    COOKIE_SECURE: bool = False
    HTTPS_ONLY: bool = False

    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "testserver"]
    RATE_LIMIT_REQUESTS: int = 120
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    AUTH_RATE_LIMIT_REQUESTS: int = 10
    MAX_UPLOAD_BYTES: int = 10 * 1024 * 1024
    AI_SPEND_CAP_USD: float = 0.0
    DEMO_ACCOUNT_EMAIL: str = "admin@aiia.gov.in"

    STORAGE_BACKEND: str = "local"
    STORAGE_LOCAL_PATH: str = "./storage"

    ANTHROPIC_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("CORS_ORIGINS", "ALLOWED_HOSTS", mode="before")
    @classmethod
    def parse_list(cls, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @model_validator(mode="after")
    def validate_production_settings(self):
        is_production = self.ENVIRONMENT.lower() == "production"
        insecure_secret = self.SECRET_KEY == "change-this-development-secret-before-production" or len(self.SECRET_KEY) < 32
        if is_production and (self.DEBUG or insecure_secret or not self.HTTPS_ONLY or not self.COOKIE_SECURE):
            raise ValueError("Production requires DEBUG=false, a strong SECRET_KEY, HTTPS_ONLY=true, and COOKIE_SECURE=true.")
        if is_production and any(not origin.startswith("https://") for origin in self.CORS_ORIGINS):
            raise ValueError("Production CORS origins must use HTTPS.")
        return self


settings = Settings()
