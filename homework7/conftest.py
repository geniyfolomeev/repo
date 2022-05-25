import os
import time
from requests.exceptions import ConnectionError
import flask_mock
import settings
from client import SocketClient
from logging.config import dictConfig


client = SocketClient(host=settings.MOCK_HOST, port=int(settings.MOCK_PORT))


def wait_ready():
    started = False
    st = time.time()
    while time.time() - st <= 5:
        try:
            response = client.make_request(params="/user")
            if response[0] == 200:
                started = True
                break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError(f'{settings.MOCK_HOST}:{settings.MOCK_PORT} did not started in 5s!')


def pytest_configure(config):

    if not hasattr(config, 'workerinput'):
        flask_mock.run_mock()
        wait_ready()
        log_path = os.path.abspath(os.path.join(os.getcwd(), "server_log.log"))

        if os.path.exists(log_path):
            os.remove(log_path)

        dictConfig({
            'version': 1,
            'handlers': {
                'file.handler': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': 'server_log.log',
                    'maxBytes': 10000000,
                    'backupCount': 5,
                    'level': 'DEBUG',
                },
            },
            'loggers': {
                'werkzeug': {
                    'level': 'DEBUG',
                    'handlers': ['file.handler'],
                },
            },
        })


def pytest_unconfigure(config):
    if not hasattr(config, 'workerinput'):
        client.make_request(params="/shutdown", shutdown=True)
