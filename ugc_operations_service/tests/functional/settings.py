from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    auth_api_url: str = "http://auth-api:8080/api/v1"
    ugc_api_url: str = "http://ugc-operations:8080/api/v1"


test_settings = TestSettings()
