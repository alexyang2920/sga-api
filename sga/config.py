from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = 'sqlite:///sga_app.db'

    model_config = SettingsConfigDict()

settings = Settings()