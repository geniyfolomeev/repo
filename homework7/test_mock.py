import time
from base import BaseCase


class TestSocket(BaseCase):

    def test_get_and_post_user(self, create_user, clear):
        response = self.client.make_request(method="POST",
                                            params="/user",
                                            data={self.user_name: self.user_surname})  # Пытаемся создать пользака
        # еще раз
        assert response[0] == 409
        status_code, headers, payload = self.client.make_request(params=f"/user/{self.user_name}")  # Получаем фамилию
        assert status_code == 200
        assert payload == self.user_surname

    def test_put_user(self, create_user, clear):
        response = self.client.make_request(params=f"/user/{self.user_name}")  # Получили фамилию пользака
        assert response[0] == 200
        assert response[-1] == self.user_surname
        new_user_surname = self.user_surname + "broken-user"  # Выбираем новую фамилию
        response = self.client.make_request(method="PUT",
                                            params="/user",
                                            data={self.user_name: new_user_surname})  # Обновляем фамилию
        assert response[0] == 200
        response = self.client.make_request(params=f"/user/{self.user_name}")  # Получаем обновленную фамилию
        assert response[0] == 200
        assert response[-1] == new_user_surname

    def test_delete_user(self, create_user):
        response = self.client.make_request(params=f"/user/{self.user_name}")  # Получили фамилию пользака
        assert response[0] == 200, f"Response: {response}"
        assert response[-1] == self.user_surname
        response = self.client.make_request(method="DELETE", params=f"/user/{self.user_name}")  # Удаляем пользователя
        assert response[0] == 200
        response = self.client.make_request(params=f"/user/{self.user_name}")  # Пробуем получить удаленного пользака
        assert response[0] == 404
        response = self.client.make_request(method="DELETE",
                                            params=f"/user/{self.user_name}")  # Пробуем удалить удаленного пользователя
        assert response[0] == 404

    def test_reset(self, create_user):
        time.sleep(2)
        response = self.client.make_request(params="/user")  # Получаем данные обо всех пользователях
        assert response[0] == 200
        assert self.user_name in response[-1]
        response = self.client.make_request(params="/reset")  # Сносим БД
        assert response[0] == 200
        response = self.client.make_request(params="/user")  # Получаем данные обо всех пользователях
        assert response[0] == 200
        assert response[-1] == '{}'
