import os
import shutil
import sys
import pytest


def pytest_addoption(parser):
    parser.addoption('--selenoid', action='store_true')


def pytest_configure(config):
    pytest.url = "http://127.0.0.1:8080"
    pytest.url_ui = "http://127.0.0.1:8080"
    pytest.mock = "http://127.0.0.1:80"

    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'

    log_api = os.path.join(os.getcwd(), "api", "logs")
    log_ui = os.path.join(os.getcwd(), "ui", "logs")
    screenshots_ui = os.path.join(os.getcwd(), "ui", "screenshots")

    if not hasattr(config, 'workerunput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)
        if os.path.exists(log_api):
            shutil.rmtree(log_api)
        os.makedirs(log_api)
        if os.path.exists(log_ui):
            shutil.rmtree(log_ui)
        os.makedirs(log_ui)
        if os.path.exists(screenshots_ui):
            shutil.rmtree(screenshots_ui)
        os.makedirs(screenshots_ui)

    config.addinivalue_line(
        "markers", "API: mark test to run only API tests"
    )
    config.addinivalue_line(
        "markers", "UI: mark test to run only UI tests"
    )
