import os

import requests
import pytest

url = f"http://{os.environ['MOCK_HOST']}:{os.environ['MOCK_PORT']}"


def test_post_get_user_main(post_user_delete_user):
    data = {"test_user": 666}
    response = requests.post(url=f"{url}/", json=data)
    assert response.status_code == 409
    data = {"test_user32": 666}
    response = requests.post(url=f"{url}/", json=data)
    assert response.status_code == 409
    data = {"test_user": 667}
    response = requests.put(url=f"{url}/", json=data)
    assert response.status_code == 200
    response = requests.get(url=f"{url}/vk_id/test_user")
    assert response.json()["vk_id"] == 667
    data = {"test_user1": 668}
    response = requests.put(url=f"{url}/", json=data)
    assert response.status_code == 201
    response = requests.delete(url=f"{url}/vk_id/test_user1")
    assert response.status_code == 200
