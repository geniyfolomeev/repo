import pytest
from client import SocketClient
import settings
from faker import Faker


class BaseCase:
    client = None
    user_name = None
    user_surname = None

    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        self.client = SocketClient(host=settings.MOCK_HOST, port=int(settings.MOCK_PORT))

    @pytest.fixture(scope="function")
    def clear(self):
        yield
        response = self.client.make_request(method="DELETE", params=f"/user/{self.user_name}")
        assert response[0] == 200

    @pytest.fixture(scope="function")
    def generate_user(self):
        fake = Faker()
        user_info = fake.name().split()
        self.user_name = user_info[0]
        self.user_surname = user_info[1]

    @pytest.fixture(scope="function")
    def create_user(self, generate_user):
        response = self.client.make_request(method="POST",
                                            params="/user",
                                            data={self.user_name: self.user_surname})  # Создаем пользователя
        assert response[0] == 200
