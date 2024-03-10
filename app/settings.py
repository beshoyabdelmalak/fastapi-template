from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    
    BASE_URL: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)

config = Settings()