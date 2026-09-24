from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Support Ticket API"
    APP_ENV: str = "development"
    PORT: int = 8000
    MONGODB_URL: str
    DATABASE_NAME: str = "support_ticket_db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()