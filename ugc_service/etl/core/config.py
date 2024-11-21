import os
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parents[1]


class BaseConfig(BaseSettings):
    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


class ClickSettings(BaseConfig):
    CONNECT: str = "localhost"
    PORT: str = "9000"
    DATABASE: str = "statistics"

    class Config:
        env_prefix = "click_"


class ETLSettings(BaseSettings):
    LOGGER_PATH: str = "ETL.log"
    CONTENT_API: str = "http://content-delivery-service:8000/api/v1/films/"
    USER_API: str = "http://auth-service:8000/api/v1/users/"
    BATCH_COUNT: int = 10

    class Config:
        env_prefix = "etl_"


class KafkaSettings(BaseSettings):
    SERVERS: list = ["127.0.0.1:9094"]

    class Config:
        env_prefix = "kafka_"
