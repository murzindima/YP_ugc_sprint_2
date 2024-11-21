from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    api_url: str = "http://localhost:8000"
    api_base_path: str = "/api/v1"


test_settings = TestSettings()
