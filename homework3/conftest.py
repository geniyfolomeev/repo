import pytest
from api_client import ApiClient
import creds


@pytest.fixture(scope="session")
def api_client():
    api_client = ApiClient(creds.email, creds.password)
    api_client.set_cookies()
    return api_client


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "API: mark test to run only API tests"
    )
