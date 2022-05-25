import shutil
import sys
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os
from _pytest.fixtures import FixtureRequest


@pytest.fixture(autouse=True)
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
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerunput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_temp_dir = base_dir


@pytest.fixture(scope='function')
def temp_dir(request: FixtureRequest):
    base_temp_dir = request.config.base_temp_dir
    test_dir = os.path.join(base_temp_dir, request.node.name)
    os.makedirs(test_dir)
    return test_dir
