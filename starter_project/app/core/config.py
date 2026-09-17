from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Book Borrowing API"
    app_env: str = "development"

    secret_key: str = "replace-me"
    jwt_secret_key: str = "replace-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    postgres_db: str = "book_borrowing"
    postgres_user: str = "postgres"
    postgres_password: str = "1234"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    database_url: str = "postgresql+asyncpg://postgres:1234@localhost:5432/book_borrowing"

    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "book_borrowing"
    mongo_logs_collection: str = "admin_activity_logs"

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
