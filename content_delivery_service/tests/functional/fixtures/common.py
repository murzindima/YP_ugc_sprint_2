import pytest

from functional.settings import test_settings


@pytest.fixture
def api_base_url():
    api_url = test_settings.api_url
    base_path = test_settings.api_base_path
    base_url = f"{api_url}{base_path}"
    return base_url
