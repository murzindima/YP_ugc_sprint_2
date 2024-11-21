from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    es_url: str = "http://localhost:9200"

    redis_host: str = "localhost"
    redis_port: int = 6379

    api_url: str = "http://localhost:8000"
    api_base_path: str = "/api/v1"


test_settings = TestSettings()
