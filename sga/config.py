import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str

    jwt_secret_key: str
    jwt_algo: str
    jwt_access_token_expires_minutes: int

    model_config = SettingsConfigDict()

    class Config:
        env_file = os.getenv('ENV_FILE', '.env.development')


settings = Settings()
