from functools import lru_cache
from typing import Annotated, Literal

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

Environment = Literal["local", "test", "staging", "production"]

# NoDecode stops pydantic-settings from JSON-parsing the raw env value, so the
# "before" validator below can accept a plain comma separated string.
CsvList = Annotated[list[str], NoDecode]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Application
    environment: Environment = "local"
    debug: bool = False
    # Separate from debug: echoing every statement drowns out the request logs.
    sql_echo: bool = False
    project_name: str = "Implesia Backend"
    api_v1_prefix: str = "/api/v1"
    cors_origins: CsvList = Field(default_factory=list)

    # Security
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 14
    jwt_algorithm: str = "HS256"

    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "implesia"
    postgres_password: str = "implesia"
    postgres_db: str = "implesia"
    database_url_override: str | None = None

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Rate limiting
    rate_limit_default: str = "200/minute"
    rate_limit_leads: str = "5/hour"
    rate_limit_orders: str = "5/hour"

    # Bootstrap superuser
    first_superuser_email: str = "admin@implesia.com"
    first_superuser_password: str = "change-me-too"

    # Email
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_tls: bool = True
    email_from: str = "no-reply@implesia.com"
    email_from_name: str = "Implesia IT"
    lead_notification_recipients: CsvList = Field(default_factory=list)

    # Cloudflare Turnstile
    turnstile_secret_key: str = ""

    @field_validator("cors_origins", "lead_notification_recipients", mode="before")
    @classmethod
    def _split_csv(cls, value: object) -> object:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @property
    def database_url(self) -> str:
        if self.database_url_override:
            return self.database_url_override
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.postgres_user,
                password=self.postgres_password,
                host=self.postgres_host,
                port=self.postgres_port,
                path=self.postgres_db,
            )
        )

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def emails_enabled(self) -> bool:
        return bool(self.smtp_host)

    @property
    def turnstile_enabled(self) -> bool:
        return bool(self.turnstile_secret_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
