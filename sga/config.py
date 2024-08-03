from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = 'sqlite+aiosqlite:///sga_app.db'

    model_config = SettingsConfigDict()

settings = Settings()