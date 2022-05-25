from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pytest


@pytest.fixture()
def browser():
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    browser.maximize_window()
    yield browser
    browser.quit()


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "UI: mark test to run only UI tests"
    )
    config.addinivalue_line(
        "markers", "skip: mark test to skip"
    )
