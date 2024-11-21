from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class PostgresSettings(BaseConfig):
    dbname: str = "postgres"
    user: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: int = 5432

    class Config:
        env_prefix = "postgres_"


class ElasticsearchSettings(BaseConfig):
    host: str = "localhost"
    port: int = 9200
    scheme: str = "http"

    class Config:
        env_prefix = "elastic_"


class StateSettings(BaseConfig):
    type: str = "json"
    json_file: str = "state.json"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    class Config:
        env_prefix = "state_"


postgres_settings = PostgresSettings()
elasticsearch_settings = ElasticsearchSettings()
state_settings = StateSettings()

MOVIES_INDEX_NAME = "movies"
MOVIES_STATE_KEY = "last_movies_updated"
PERSONS_INDEX_NAME = "persons"
PERSONS_STATE_KEY = "last_persons_updated"
GENRES_INDEX_NAME = "genres"
GENRES_STATE_KEY = "last_genres_updated"
TIMEOUT = 20
