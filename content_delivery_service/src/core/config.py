import os
from logging import config as logging_config

from pydantic_settings import BaseSettings

from core.logger import LOGGING

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MOVIES_INDEX = "movies"
PERSONS_INDEX = "persons"
GENRES_INDEX = "genres"


class BaseConfig(BaseSettings):
    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


class AppSettings(BaseConfig):
    log_level: str = "INFO"
    batch_size: int = 100
    project_name: str = "movies"
    enable_tracer: bool = os.getenv("ENABLE_TRACER", default="True").lower() == "true"

    class Config:
        env_prefix = "app_"


class ElasticsearchSettings(BaseConfig):
    host: str = "localhost"
    port: int = 9200
    scheme: str = "http"

    class Config:
        env_prefix = "elastic_"


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


elasticsearch_settings = ElasticsearchSettings()
redis_settings = RedisSettings()
jaeger_settings = JaegerSettings()
app_settings = AppSettings()
logging_config.dictConfig(LOGGING)
