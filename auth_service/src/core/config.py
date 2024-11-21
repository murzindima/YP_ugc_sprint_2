import os
from logging import config as logging_config
from pathlib import Path

from pydantic_settings import BaseSettings

from src.core.logger import LOGGING

BASE_DIR = Path(__file__).resolve().parents[2]


class BaseConfig(BaseSettings):
    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


class AppSettings(BaseConfig):
    log_level: str = "INFO"
    project_name: str = "Auth Service"
    pagination_size: int = 100
    authjwt_secret_key: str = "secretsecret"
    authjwt_denylist_enabled: bool = (
        os.getenv("AUTHJWT_DENYLIST_ENABLED", default="True").lower() == "true"
    )
    authjwt_denylist_token_checks: set = {"access"}
    access_token_expires: int = 15 * 60  # 15 minutes
    refresh_token_expires: int = 60 * 60 * 24 * 30  # 30 days
    enable_tracer: bool = os.getenv("ENABLE_TRACER", default="True").lower() == "true"

    class Config:
        env_prefix = "app_"


class PostgresSettings(BaseConfig):
    db: str = "auth_database"
    user: str = "app"
    password: str = "pass"
    host: str = "localhost"
    port: int = 5432
    echo: bool = True

    class Config:
        env_prefix = "postgres_"


class RedisSettings(BaseConfig):
    host: str = "localhost"
    port: int = 6379
    db: int = 0

    class Config:
        env_prefix = "redis_"


class JaegerSettings(BaseConfig):
    host: str = "localhost"
    port: int = 6831

    class Config:
        env_prefix = "jaeger_"


class OAuth2Settings(BaseConfig):
    client_id: str = "client_id_1234"
    client_secret: str = "client_secret_1234"
    redirect_uri: str = "http://localhost:8000/oauth2callback"
    auth_server: str = "http://oauth2-server"
    resource_server: str = "http://resource-server"

    class Config:
        env_prefix = "oauth_"


app_settings = AppSettings()
redis_settings = RedisSettings()
postgres_settings = PostgresSettings()
jaeger_settings = JaegerSettings()
oauth2_settings = OAuth2Settings()
logging_config.dictConfig(LOGGING)
