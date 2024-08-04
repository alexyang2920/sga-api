from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # database_url: str = 'sqlite+aiosqlite:///sga_app.db'
    database_url: str = 'postgresql+asyncpg://sga:Temp1234@localhost:5432/sga'

    # To get a string like this run: openssl rand -hex 32
    jwt_secret_key: str = '10c6b69df90c84ed7253106f928c39553141ad644a61c28a059251ea1763f8b3'
    jwt_algo: str = 'HS256'
    jwt_access_token_expires_minutes: int = 24 * 60

    model_config = SettingsConfigDict()


settings = Settings()
