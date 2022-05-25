import pytest
import requests


class ApiClient:
    def __init__(self):
        self.session = requests.Session()
        self.welcome_url = f"{pytest.url}/welcome/"
        self.authorization_url = f"{pytest.url}/login"
        self.add_user_url = f"{pytest.url}/api/user"
        self.status_url = f"{pytest.url}/status"
        self.reg_user_url = f"{pytest.url}/reg"
        self.logout_url = f"{pytest.url}/logout"
        self.mock_url = pytest.mock

    def authorize(self, user_data):
        data = {
            "username": user_data["username"],
            "password": user_data["password"],
            "submit": "Login"
        }
        return self.session.post(self.authorization_url, json=data)

    def post_user(self, user_data):
        return self.session.post(self.add_user_url, json=user_data)

    def delete_user(self, username):
        return self.session.delete(f"{self.add_user_url}/{username}")

    def check_status(self):
        return self.session.get(self.status_url)

    def change_password(self, username, data):
        return self.session.put(f"{self.add_user_url}/{username}/change-password", json=data)

    def block_user(self, username, data):
        return self.session.post(f"{self.add_user_url}/{username}/block", json=data)

    def unlock_user(self, username, data):
        return self.session.post(f"{self.add_user_url}/{username}/accept", json=data)

    def reg_user(self, data, confirm_password=None, term="y", register="Register"):
        load = {
            "name": data["name"],
            "surname": data["surname"],
            "middlename": data["middle_name"],
            "username": data["username"],
            "email": data["email"],
            "password": data["password"],
            "confirm": data["password"] if confirm_password is None else confirm_password,
            "term": term,
            "submit": register,
                }
        return self.session.post(url=self.reg_user_url, json=load)

    def post_user_mock(self, username, user_id):
        data = {
            username: user_id
        }
        return self.session.post(url=self.mock_url, json=data)

    def delete_user_mock(self, username):
        return self.session.delete(url=f"{self.mock_url}/vk_id/{username}")

    def get_all_users_mock(self):
        return self.session.get(self.mock_url)

    def get_user_mock(self, username):
        return self.session.get(url=f"{self.mock_url}/vk_id/{username}")

    def logout(self):
        return self.session.get(url=self.logout_url)

    def get_main_page(self):
        return self.session.get(url=self.welcome_url)
