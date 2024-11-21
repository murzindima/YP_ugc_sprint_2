import os
from logging import config as logging_config
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from src.core.logger import LOGGING

BASE_DIR = Path(__file__).resolve().parents[3]

load_dotenv()


class BaseConfig(BaseSettings):
    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


class AppSettings(BaseConfig):
    log_level: str = "INFO"
    project_name: str = "UGC Operations Service"
    pagination_size: int = 100
    authjwt_secret_key: str = "secretsecret"

    class Config:
        env_prefix = "app_"


class SentrySettings(BaseConfig):
    enable_sdk: bool = os.getenv("SENTRY_ENABLE_SDK", default="False").lower() == "true"
    enable_tracing: bool = (
        os.getenv("SENTRY_ENABLE_TRACING", default="False").lower() == "true"
    )
    dsn: str = "your-sentry-dsn"
    traces_sample_rate: float = 1.0
    profiles_sample_rate: float = 1.0

    class Config:
        env_prefix = "sentry_"


class MongoSettings(BaseConfig):
    db: str = "ugc_operations_database"
    host: str = "localhost"
    port: int = 27017

    collection_like: str = "liked_films"
    collection_bookmarks: str = "bookmarks_films"
    collection_reviewed: str = "reviewed_films"

    user: str = "app"
    password: str = "pass"

    class Config:
        env_prefix = "mongo_"
        extra = "allow"


class JaegerSettings(BaseConfig):
    enable_tracer: bool = (
        os.getenv("JAEGER_ENABLE_TRACER", default="False").lower() == "true"
    )
    host: str = "localhost"
    port: int = 6831

    class Config:
        env_prefix = "jaeger_"
        extra = "allow"


app_settings = AppSettings()
mongo_settings = MongoSettings()
jaeger_settings = JaegerSettings()
sentry_settings = SentrySettings()
logging_config.dictConfig(LOGGING)
