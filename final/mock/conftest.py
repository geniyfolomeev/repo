import os

import pytest
import requests

url = f"http://{os.environ['MOCK_HOST']}:{os.environ['MOCK_PORT']}"


@pytest.fixture(scope="function")
def post_user_delete_user():
    data = {"test_user": 666}
    response = requests.post(url=f"{url}/", json=data)
    assert response.status_code == 200
    response = requests.get(url=f"{url}/vk_id/test_user")
    assert response.status_code == 200
    assert response.json()["vk_id"] == 666
    yield
    response = requests.delete(url=f"{url}/vk_id/test_user")
    assert response.status_code == 200
    response = requests.get(url=f"{url}/vk_id/test_user")
    assert response.status_code == 404
    response = requests.delete(url=f"{url}/vk_id/test_user")
    assert response.status_code == 404
