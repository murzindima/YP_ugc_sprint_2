import os
from logging import config as logging_config
from pathlib import Path

from pydantic_settings import BaseSettings

from app.core.logger import LOGGING

BASE_DIR = Path(__file__).resolve().parents[2]  # TODO: parents[3] for a docker env


class BaseConfig(BaseSettings):
    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


class AppSettings(BaseConfig):
    debug: bool = os.getenv("DEBUG", default="True").lower() == "true"
    log_level: str = "INFO"
    log_path: str = "/app/.venv/logs/ugc.log"
    app_name: str = "UGC API"
    project_name: str = "UGC Service"
    jwt_secret_key: str = "secretsecret"

    class Config:
        env_prefix = "app_"
        extra = "allow"


class KafkaSettings(BaseConfig):
    bootstrap_servers: str
    likes_topic: str
    comments_topic: str
    clicks_topic: str
    bookmarks_topic: str
    movie_filter_requests_topic: str
    movie_player_changes_topic: str
    movie_watch_times_topic: str

    class Config:
        env_prefix = "kafka_"
        extra = "allow"


authorizations = {
    "jsonWebToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
    }
}

app_settings = AppSettings()
kafka_settings = KafkaSettings()
logging_config.dictConfig(LOGGING)
