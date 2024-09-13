from typing import List, ClassVar
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")
    OPENAI_API_KEY: str
    PROJECT_NAME: str
    DB_NAME: str
    FASTAPI_ENVIRONMENT: str
    BACKEND_CORS_ORIGINS:List[str]

settings = Settings()

print(settings.dict())