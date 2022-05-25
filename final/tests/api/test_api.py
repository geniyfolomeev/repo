import random
import pytest
from tests import base
import allure
import requests


class TestApiCodes(base.BaseCase):

    @pytest.mark.API
    @pytest.mark.parametrize("random_length, correct_validation", [(True, True), (False, False)])
    def test_add_user_f(self, random_length, correct_validation, setup, delete_user_db):
        """Тест проверяет ответы приложения при создании пользователя по API, а также проверяется соответствие валидации
        на фронтенде и валидации внутри БД."""
        with allure.step("Добавляем пользователя, проверяем ответ приложения."):
            response = self.api_client.post_user(self.generate_user_data(random_length=random_length,
                                                                         correct_validation=correct_validation))

            assert response.json().get("detail") == "User was added", f"User {self.user_data['username']} was not " \
                                                                      f"added.\nResponse: {response.status_code}\n" \
                                                                      f"Should be: 201 "
            # BUG: app returns 500 due to wrong frontend validation
            assert response.json().get("status") == "success"
            assert response.status_code == 201, f"Wrong response status code: {response.status_code}, should be: 201"
            # BUG: app returns 210 when created

    @pytest.mark.API
    def test_add_user_again_f(self, setup, delete_user_db):
        """Тест проверяет ответ приложения при повторном создании пользователя по API."""
        with allure.step("Добавляем пользователя."):
            self.api_client.post_user(user_data=self.generate_user_data())
        with allure.step("Пытаемся добавить уже существующего пользователя, проверяем ответ приложения."):
            response = self.api_client.post_user(self.user_data)

            assert response.json().get("detail") == "User already exists"
            assert response.status_code == 304, f"Wrong response status code: {response.status_code}, should be: 304"
            # BUG: app returns 400 when user already exists

    @pytest.mark.API
    def test_delete_user_f(self, setup):
        """Тест проверяет ответ приложения при удалении пользователя по API."""
        with allure.step("Добавляем пользователя."):
            self.api_client.post_user(self.generate_user_data())
        with allure.step("Удаляем пользователя, проверяем ответ приложения."):
            response = self.api_client.delete_user(username=self.user_data["username"])

            assert response.status_code == 204
            assert response.text != ""      # BUG: empty response

    @pytest.mark.API
    def test_bad_request_f(self, setup):
        """Тест проверяет ответ приложения при некорректном API запросе."""
        with allure.step("Удаляем из запроса на создание пользователя поле password."):
            user_data = self.generate_user_data().pop("password")
        with allure.step("Пытаемся добавить пользователя, посредством некорректного API запроса."
                         "Проверяем ответ приложения."):
            response = self.api_client.post_user(user_data)

            assert response.status_code == 400, f"Wrong response status code: {response.status_code}, should be: 400"
            # BUG: app returns 500 when bad request

    @pytest.mark.API
    def test_does_not_exist(self, setup):
        """Тест проверяет ответ приложения при удалении несуществующего пользователя по API."""
        with allure.step("Пробуем удалить несуществующего пользователя, проверяем ответ приложения."):
            response = self.api_client.delete_user(username=self.generate_user_data()["username"])

            assert response.json().get("detail") == "User does not exist!"
            assert response.status_code == 404

    @pytest.mark.API
    def test_unauthorized(self, setup):
        """Тест проверяет ответ приложения при регистрации пользователя по API без предварительной авторизации."""
        with allure.step("Пытаемся добавить пользователя, не авторизовавшись в приложении."
                         "Проверяем ответ приложения."):
            response = requests.post(url=f"{pytest.url}/login", json=self.generate_user_data())

            assert response.status_code == 401

    @pytest.mark.API
    def test_check_status(self, setup):
        """Тест проверяет ответ приложения при проверке его статуса по API"""
        with allure.step("Запрашиваем статус приложения, проверяем полученный ответ."):
            response = self.api_client.check_status()

            assert response.status_code == 200
            assert response.json().get("status") == "ok"

    @pytest.mark.API
    def test_post_user_email_f(self, setup, delete_user_db):
        """Тест проверяет ответ приложения при добавлении пользователя с некорректным email (без @mail.ru)."""
        with allure.step("Регистрируем пользователя с почтой, не имеющей на конце @mail.ru"):
            data = self.generate_user_data()
            data["email"] = self.generate_value(stop=64, random_length=True)
            response = self.api_client.post_user(user_data=data)

            assert response.status_code == 400, f"Wrong response: {response.status_code}, should be 400."


class TestApiDatabase(base.BaseCase):

    @pytest.mark.API
    @pytest.mark.parametrize("add_middle_name, random_length, correct_validation", [(True, True, True),
                                                                                    (False, True, True),
                                                                                    (True, False, False)])
    def test_post_user_check_db_f(self, add_middle_name, random_length, correct_validation, setup, delete_user_db):
        """Тест проверяет данные о пользователе, записанные в БД посредством POST запроса."""
        with allure.step(f"Добавляем пользователя, проверяем запись в БД его данных. Наличие отчества: "
                         f"{add_middle_name}, случайная длина полей: {random_length}, длина полей не превышает"
                         f" выделенного в БД места {correct_validation}."):
            self.api_client.post_user(user_data=self.generate_user_data(add_middle_name=add_middle_name,
                                                                        random_length=random_length,
                                                                        correct_validation=correct_validation))
            table = self.get_row(username=self.user_data["username"])

            assert table is not None, "No such user in database"  # BUG: no such row in db because of too much symbols
            assert table["name"] == self.user_data["name"], f"Wrong name in DB.\nShould be:{self.user_data['name']}\n" \
                                                            f"Got: {table['name']}"
            assert table["surname"] == self.user_data["surname"], f"Wrong surname in DB.\nShould " \
                                                                  f"be:{self.user_data['surname']}\n" \
                                                                  f"Got: {table['surname']}"
            assert table["middle_name"] == self.user_data["middle_name"], f"Wrong middle name in DB.\nShould be:" \
                                                                          f"{self.user_data['middle_name']}\n" \
                                                                          f"Got: {table['middle_name']}"
            # BUG: no middle name in DB
            assert table["password"] == self.user_data["password"], f"Wrong password in DB.\nShould be:" \
                                                                    f"{self.user_data['password']}\n" \
                                                                    f"Got: {table['password']}"
            assert table["email"] == self.user_data["email"], f"Wrong email in DB.\n" \
                                                              f"Should be:{self.user_data['email']}\n" \
                                                              f"Got: {table['email']}"
            assert table["access"] == 1, f"Wrong access flag in DB.\nShould be: 1\nGot: {table['access']}"

    @pytest.mark.API
    def test_delete_user_check_db(self, setup):
        """Тест проверяет отсутствие пользователя в БД, после выполнения DELETE запроса."""
        with allure.step("Добавляем пользователя, проверяем, что в БД добавилась строка для указанного логина."):
            self.api_client.post_user(user_data=self.generate_user_data())
            assert self.get_row(username=self.user_data["username"]) is not None
        with allure.step("Удаляем пользователя, проверяем, что в БД отсутствует запись для данного логина."):
            self.api_client.delete_user(username=self.user_data["username"])
            assert self.get_row(username=self.user_data["username"]) is None

    @pytest.mark.API
    @pytest.mark.parametrize("stop, status_code", [(0, 400), (1, 204), (2, 204), (100, 204), (254, 204), (255, 204),
                                                   (256, 400)])
    def test_change_password_code_f(self, stop, status_code, setup, delete_user_db):
        """Тест проверяет ответ приложения при запросе на изменение пароля пользователя."""
        with allure.step(f"Добавляем пользователя."):
            self.api_client.post_user(user_data=self.generate_user_data())
        with allure.step("Меняем пользователю пароль API запросом, проверяем ответ приложения."
                         f" Длина пароля: {stop}, ожидаемый ответ приложения: {status_code}."):
            self.user_data["password"] = self.generate_value(stop=stop, random_length=False)
            response = self.api_client.change_password(username=self.user_data["username"], data=self.user_data)

            assert response.status_code == status_code, f"Wrong status code: {response.status_code}\nExpected: " \
                                                        f"{status_code}\nBecause of password`s length = " \
                                                        f"{len(self.user_data['password'])}"
            # BUG: successful status code when password is invalid

    @pytest.mark.API
    @pytest.mark.parametrize("stop", [0, 1, 2, 100, 254, 255, 256])
    def test_change_password_db_f(self, stop, setup, delete_user_db):
        """Тест проверяет изменение пароля у пользователя (запись в БД), после соответствующего API запроса."""
        with allure.step("Добавляем пользователя."):
            self.api_client.post_user(user_data=self.generate_user_data())
            password_old = self.get_row(self.user_data["username"])["password"]
        with allure.step("Меняем пользователю пароль API запросом, проверяем запись в БД."):
            self.user_data["password"] = self.generate_value(stop=stop, random_length=False)
            self.api_client.change_password(username=self.user_data["username"], data=self.user_data)
            password_new = self.get_row(self.user_data["username"])["password"]

            assert self.user_data["password"] == password_new, f"Incorrect password.\nExpected:" \
                                                               f" {self.user_data['password']}\nGot: {password_new}"
            assert password_old != password_new
            assert password_new is not None, f"Invalid password`s length for password: {password_new}"
            # BUG: can change password to password with invalid length

    @pytest.mark.API
    def test_change_password_diff(self, setup, delete_user_db):
        """Тест проверяет невозможность изменения пароля пользователя посредством API запроса в ситуации, когда
        новый пароль аналогичен старому."""
        with allure.step("Добавляем пользователя."):
            self.api_client.post_user(user_data=self.generate_user_data())
        with allure.step("Меняем пользователю пароль API запросом, указав новый пароль, аналогичный старому. "
                         "Проверяем ответ приложения и запись в БД."):
            response = self.api_client.change_password(username=self.user_data["username"], data=self.user_data)

            assert response.status_code == 400
            assert response.json().get("status") == "failed"
            assert self.get_row(self.user_data["username"])["password"] == self.user_data["password"]

    @pytest.mark.API
    def test_block_user_code_f(self, setup, delete_user_db):
        """Тест проверяет ответ приложения при блокировке пользователя посредством API запроса."""
        with allure.step("Добавляем пользователя."):
            self.api_client.post_user(user_data=self.generate_user_data())
        with allure.step("Блокируем добавленного пользователя, проверяем ответ приложения."):
            response = self.api_client.block_user(username=self.user_data["username"], data=self.user_data)

            assert response.status_code == 200
            assert response.json().get("status") != "", "Response status is empty"  # BUG: empty response status

    @pytest.mark.API
    def test_block_user_db(self, setup, delete_user_db):
        """Тест проверяет проставление пользователю в БД флага access=0 при его блокировке посредством API запроса."""
        with allure.step("Добавляем пользователя."):
            self.api_client.post_user(user_data=self.generate_user_data())
        with allure.step("Блокируем добавленного пользователя, проверяем запись в БД."):
            self.api_client.block_user(username=self.user_data["username"], data=self.user_data)

            assert self.get_row(username=self.user_data["username"])["access"] == 0

    @pytest.mark.API
    def test_unlock_user_response_f(self, setup, delete_user_db):
        """Тест проверяет ответ приложения при получении запроса на разблокировку пользователя."""
        with allure.step("Добавляем пользователя."):
            self.api_client.post_user(user_data=self.generate_user_data())
        with allure.step("Блокируем добавленного пользователя."):
            self.api_client.block_user(username=self.user_data["username"], data=self.user_data)
        with allure.step("Выполняем запрос на разблокировку пользователя, проверяем ответ приложения."):
            response = self.api_client.unlock_user(username=self.user_data["username"], data=self.user_data)

            assert response.status_code == 200
            assert response.json().get("status") != "failed", f"Wrong response message for 200 OK: " \
                                                              f"{response.json().get('status')}"
            # BUG: wrong status for 200 status code

    @pytest.mark.API
    def test_unlock_user(self, setup, delete_user_db):
        """Тест проверяет проставление пользователю в БД флага access=1 при его разблокировке
        посредством API запроса."""
        with allure.step("Добавляем пользователя."):
            self.api_client.post_user(user_data=self.generate_user_data())
        with allure.step("Блокируем добавленного пользователя."):
            self.api_client.block_user(username=self.user_data["username"], data=self.user_data)
        with allure.step("Выполняем запрос на разблокировку пользователя, проверяем запись в БД."):
            self.api_client.unlock_user(username=self.user_data["username"], data=self.user_data)

            assert self.get_row(username=self.user_data["username"])["access"] == 1

    @pytest.mark.API
    @pytest.mark.parametrize("param, stop", [("name", 0), ("name", 46), ("name", 100), ("name", 255), ("name", 301),
                                             ("surname", 0), ("surname", 301),
                                             ("middle_name", 256),
                                             ("username", 0), ("username", 1), ("username", 5), ("username", 17),
                                             ("email", 0), ("email", 1), ("email", 5), ("email", 65),
                                             ("password", 0), ("password", 256)])
    def test_add_user_invalid_param_code_f(self, param, stop, setup, delete_user_db):
        """Тест проверяет ответ приложения при запросе на регистрацию пользователя, содержащем поле недопустимой
        длины."""
        with allure.step(f"Регистрируем пользователя с полем {param} недопустимой длины: {stop}. "
                         f"Проверяем наличие клиентской ошибки в ответе приложения."):
            data = self.generate_user_data()
            data[param] = self.generate_value(stop=stop, random_length=False)
            response = self.api_client.post_user(user_data=data)

            assert response.status_code == 400, f"Wrong response code: {response.status_code}, should be: 400"

    @pytest.mark.API
    @pytest.mark.parametrize("param, stop", [("name", 0), ("name", 46), ("name", 100), ("name", 255), ("name", 301),
                                             ("surname", 0), ("surname", 301),
                                             ("middle_name", 256),
                                             ("username", 0), ("username", 1), ("username", 5), ("username", 17),
                                             ("email", 0), ("email", 1), ("email", 5), ("email", 65),
                                             ("password", 0), ("password", 256)])
    def test_add_user_invalid_param_db_f(self, param, stop, setup, delete_user_db):
        """Тест проверяет запись в БД при запросе на регистрацию пользователя, содержащем поле недопустимой длины."""
        with allure.step(f"Регистрируем пользователя с полем {param} недопустимой длины: {stop}. "
                         f"Проверяем отсутствие записи о клиенте в БД."):
            data = self.generate_user_data()
            data[param] = self.generate_value(stop=stop, random_length=False)
            self.api_client.post_user(user_data=data)

            assert self.get_row(username=self.user_data["username"]) is None, f"Created user {data['username']} " \
                                                                              f"with invalid {param} = {data[param]}"

    @pytest.mark.API
    @pytest.mark.parametrize("param, stop", [("name", 1), ("name", 2), ("name", 20), ("name", 44), ("name", 45),
                                             ("surname", 1), ("surname", 2), ("surname", 150), ("surname", 299),
                                             ("surname", 300),
                                             ("middle_name", 0), ("middle_name", 100), ("middle_name", 255),
                                             ("username", 6), ("username", 7), ("username", 11), ("username", 15),
                                             ("username", 16),
                                             ("email", 6), ("email", 7), ("email", 34), ("email", 63), ("email", 64),
                                             ("password", 1), ("password", 255)])
    def test_add_user_valid_param_code_f(self, param, stop, setup, delete_user_db):
        """Тест проверяет ответ приложения при запросе на регистрацию пользователя с валидным заполнением полей."""
        with allure.step(f"Регистрируем пользователя с полем {param} валидной длины: {stop}. "
                         f"Проверяем ответ приложения."):
            data = self.generate_user_data()
            data[param] = self.generate_value(stop=stop, random_length=False)
            response = self.api_client.post_user(user_data=data)

            assert response.status_code == 201, f"Wrong status code: {response.status_code}, should be 201."
            # BUG: wrong status code

    @pytest.mark.API
    @pytest.mark.parametrize("param, stop", [("name", 1), ("name", 2), ("name", 20), ("name", 44), ("name", 45),
                                             ("surname", 1), ("surname", 2), ("surname", 150), ("surname", 299),
                                             ("surname", 300),
                                             ("middle_name", 0), ("middle_name", 100), ("middle_name", 255),
                                             ("username", 6), ("username", 7), ("username", 11), ("username", 15),
                                             ("username", 16),
                                             ("email", 6), ("email", 7), ("email", 34), ("email", 63), ("email", 64),
                                             ("password", 1), ("password", 255)])
    def test_add_user_valid_param_db_f(self, param, stop, setup, delete_user_db):
        """Тест проверяет запись в БД при запросе на регистрацию пользователя с валидным заполнением полей."""
        with allure.step(f"Регистрируем пользователя с полем {param} валидной длины: {stop}. "
                         f"Проверяем запись в БД."):
            data = self.generate_user_data()
            data[param] = self.generate_value(stop=stop, random_length=False)
            self.api_client.post_user(user_data=data)
            table = self.get_row(username=self.user_data["username"])
            assert table is not None, f"No such user: {self.user_data['username']} in database"
            assert table[param] == data[param]

    @pytest.mark.API
    def test_post_user_email_db_f(self, setup, delete_user_db):
        """Тест проверяет запись в БД при добавлении пользователя с некорректным email (без @mail.ru)."""
        with allure.step("Регистрируем пользователя с почтой, не имеющей на конце @mail.ru"):
            data = self.generate_user_data()
            data["email"] = self.generate_value(stop=64, random_length=True)
            self.api_client.post_user(user_data=data)

            assert self.get_row(username=data["username"]) is None, f"Added user: {data['username']} with " \
                                                                    f"invalid email: {data['email']}"


class TestRegUser(base.BaseCase):

    @pytest.mark.API
    @pytest.mark.parametrize("middle_name", [True, False])
    def test_add_user_reg(self, middle_name, setup, delete_user_db):
        """Тест проверяет ответ приложения, при получении запроса на регистрацию пользователя."""
        with allure.step("Регистрируем пользователя, проверяем ответ приложения и редирект на главную страницу."):
            response = self.api_client.reg_user(data=self.generate_user_data(add_middle_name=middle_name))

            assert response.status_code == 200, f"Wrong status code: {response.status_code}, should be 200"
            assert response.url == self.api_client.welcome_url, f"Wrong redirect url: {response.url}\nShould be:" \
                                                                f" {self.api_client.welcome_url}"

    @pytest.mark.API
    @pytest.mark.parametrize("middle_name", [True, False])
    def test_add_user_reg_db_f(self, middle_name, setup, delete_user_db):
        """Тест проверяет корректность внесенных в БД данных о зарегистрированном пользователе."""
        with allure.step("Регистрируем пользователя, проверяем корректность внесенных в БД данных."):
            self.api_client.reg_user(data=self.generate_user_data(add_middle_name=middle_name))

            table = self.get_row(username=self.user_data["username"])

            assert table is not None, "No such user in database"
            assert table["name"] == self.user_data["name"], f"Wrong name in DB.\nShould be:{self.user_data['name']}\n" \
                                                            f"Got: {table['name']}"
            assert table["surname"] == self.user_data["surname"], f"Wrong surname in DB.\nShould " \
                                                                  f"be:{self.user_data['surname']}\n" \
                                                                  f"Got: {table['surname']}"
            assert table["middle_name"] == self.user_data["middle_name"], f"Wrong middle name in DB.\nShould be:" \
                                                                          f"{self.user_data['middle_name']}\n" \
                                                                          f"Got: {table['middle_name']}"
            # BUG: no middle name in DB
            assert table["password"] == self.user_data["password"], f"Wrong password in DB.\nShould be:" \
                                                                    f"{self.user_data['password']}\n" \
                                                                    f"Got: {table['password']}"
            assert table["email"] == self.user_data["email"], f"Wrong email in DB.\n" \
                                                              f"Should be:{self.user_data['email']}\n" \
                                                              f"Got: {table['email']}"
            assert table["access"] == 1, f"Wrong access flag in DB.\nShould be: 1\nGot: {table['access']}"

    @pytest.mark.API
    @pytest.mark.parametrize("param, stop", [("name", 0), ("name", 46), ("name", 100), ("name", 255), ("name", 301),
                                             ("surname", 0), ("surname", 301),
                                             ("middle_name", 256),
                                             ("username", 0), ("username", 1), ("username", 5), ("username", 17),
                                             ("email", 0), ("email", 1), ("email", 5), ("email", 65),
                                             ("password", 0), ("password", 256)])
    def test_reg_user_invalid_param_code_f(self, param, stop, setup, delete_user_db):
        """Тест проверяет ответ приложения при запросе на регистрацию пользователя, содержащем поле недопустимой
        длины."""
        with allure.step(f"Регистрируем пользователя с полем {param} недопустимой длины: {stop}. "
                         f"Проверяем наличие клиентской ошибки в ответе приложения."):
            data = self.generate_user_data()
            data[param] = self.generate_value(stop=stop, random_length=False)
            response = self.api_client.reg_user(data=data)

            assert response.status_code == 400, f"Wrong response code: {response.status_code}, should be: 400"

    @pytest.mark.API
    @pytest.mark.parametrize("param, stop", [("name", 0), ("name", 46), ("name", 100), ("name", 255), ("name", 301),
                                             ("surname", 0), ("surname", 301),
                                             ("middle_name", 256),
                                             ("username", 0), ("username", 1), ("username", 5), ("username", 17),
                                             ("email", 0), ("email", 1), ("email", 5), ("email", 65),
                                             ("password", 0), ("password", 256)])
    def test_reg_user_invalid_param_db_f(self, param, stop, setup, delete_user_db):
        """Тест проверяет запись в БД при запросе на регистрацию пользователя, содержащем поле недопустимой длины."""
        with allure.step(f"Регистрируем пользователя с полем {param} недопустимой длины: {stop}. "
                         f"Проверяем отсутствие записи о клиенте в БД."):
            data = self.generate_user_data()
            data[param] = self.generate_value(stop=stop, random_length=False)
            self.api_client.reg_user(data=data)
            row = self.get_row(username=self.user_data["username"])

            assert row is None, f"Created user {row['username']} with invalid {param} = {row[param]}"

    @pytest.mark.API
    @pytest.mark.parametrize("param, stop", [("name", 1), ("name", 2), ("name", 20), ("name", 44), ("name", 45),
                                             ("surname", 1), ("surname", 2), ("surname", 150), ("surname", 299),
                                             ("surname", 300),
                                             ("middle_name", 0), ("middle_name", 100), ("middle_name", 255),
                                             ("username", 6), ("username", 7), ("username", 11), ("username", 15),
                                             ("username", 16),
                                             ("email", 6), ("email", 7), ("email", 34), ("email", 63), ("email", 64),
                                             ("password", 1), ("password", 255)])
    def test_reg_user_valid_param_code_f(self, param, stop, setup, delete_user_db):
        """Тест проверяет ответ приложения при запросе на регистрацию пользователя с валидным заполнением полей."""
        with allure.step(f"Регистрируем пользователя с полем {param} валидной длины: {stop}. "
                         f"Проверяем ответ приложения."):
            data = self.generate_user_data()
            if param == "email":
                data[param] = self.generate_value(stop=stop, random_length=False, email=True)
            else:
                data[param] = self.generate_value(stop=stop, random_length=False)
            response = self.api_client.reg_user(data=data)

            assert response.status_code == 200, f"Wrong status code: {response.status_code}, should be 201.\n{param}" \
                                                f" = {data[param]}\nResponse: {response.status_code}\nRequest:" \
                                                f" {response.request.body}"
            # BUG: wrong status code

    @pytest.mark.API
    @pytest.mark.parametrize("param, stop", [("name", 1), ("name", 2), ("name", 20), ("name", 44), ("name", 45),
                                             ("surname", 1), ("surname", 2), ("surname", 150), ("surname", 299),
                                             ("surname", 300),
                                             ("middle_name", 1), ("middle_name", 100), ("middle_name", 255),
                                             ("username", 6), ("username", 7), ("username", 11), ("username", 15),
                                             ("username", 16),
                                             ("email", 6), ("email", 7), ("email", 34), ("email", 63), ("email", 64),
                                             ("password", 1), ("password", 255)])
    def test_reg_user_valid_param_db_f(self, param, stop, setup, delete_user_db):
        """Тест проверяет запись в БД при запросе на регистрацию пользователя с валидным заполнением полей."""
        with allure.step(f"Регистрируем пользователя с полем {param} валидной длины: {stop}. "
                         f"Проверяем запись в БД."):
            data = self.generate_user_data()
            if param == "email":
                data[param] = self.generate_value(stop=stop, random_length=False, email=True)
            else:
                data[param] = self.generate_value(stop=stop, random_length=False)
            response = self.api_client.reg_user(data=data)
            table = self.get_row(username=self.user_data["username"])
            assert table is not None, f"No such user: {self.user_data['username']} in database.\n{param} = " \
                                      f"{data[param]}\nResponse: {response.status_code}\nRequest:" \
                                      f" {response.request.body}"
            assert table[param] == data[param]


class TestMockApi(base.BaseCase):

    @pytest.mark.API
    def test_mock_add_delete(self):
        """Тест проверяет возможность добавления пользователей в базу мока, а также возможность их удаления."""
        with allure.step(f"Добавляем пользователя в БД мока, проверяем ответ."):
            self.generate_user_data(ui_form=True, correct_validation=True)
            response = self.api_client.post_user_mock(username=self.user_data["username"],
                                                      user_id=random.randint(0, 999999999))
            assert response.status_code == 200
        with allure.step(f"Получаем список всех пользователей из БД мока. Проверям ответ сервера и наличие "
                         f"добавленного пользователя в списке всех пользователей."):
            response = self.api_client.get_all_users_mock()
            assert response.status_code == 200
            assert self.user_data["username"] in response.json()
        with allure.step(f"Удаляем пользователя из БД мока, проверяем ответ."):
            response = self.api_client.delete_user_mock(username=self.user_data["username"])
            assert response.status_code == 200
        with allure.step(f"Получаем список всех пользователей из БД мока. Проверям ответ сервера и отсутствие "
                         f"удаленного пользователя в списке всех пользователей."):
            users = self.api_client.get_all_users_mock().json()
            assert self.user_data["username"] not in users

    @pytest.mark.API
    def test_get_user(self, setup, add_to_mock):
        """Тест проверяет корректность получаемых от мока ответов при запросе на получение существующего
        пользователя и запросе на получение несуществующего пользователя."""
        with allure.step(f"Получаем существующего пользователя из мока, проверяем корректность ответа."):
            response = self.api_client.get_user_mock(username=setup["username"])
            assert response.status_code == 200
            assert response.headers.get("Content-Type") == "application/json"
            assert response.json().get("vk_id") == self.vk_id
        with allure.step(f"Пробуем получить несуществующего пользователя из мока, проверяем корректность ответа."):
            response = self.api_client.get_user_mock(username=self.generate_value(stop=30))
            assert response.status_code == 404
            assert response.headers.get("Content-Type") == "application/json"
            assert response.json() == {}


class TestLoginApi(base.BaseCase):

    @pytest.mark.API
    def test_login_negative(self):
        """Тест проверяет ответ приложения при авторизации с некорректными данными."""
        with allure.step(f"Отправляем запрос на авторизацию в точку /login с невалидными кредами. Проверяем получение"
                         f" 401 кода."):
            data = {
                "username": self.generate_value(start=6, stop=16),
                "password": self.generate_value(start=1, stop=255),
                "submit": "Login"
            }
            response = requests.post(url=f"{pytest.url}/login", json=data)
            assert response.status_code == 401


class TestAccessApi(base.BaseCase):

    @pytest.mark.API
    def test_access_f(self, setup):
        """Тест проверяет невозможность зайти на главную страницу приложения без флага access=1 в БД"""
        with allure.step(f"Получаем информацию о пользователе, проверяем, что в БД у него access != 1."):
            user_access = self.get_row(username=setup["username"])["access"]
            assert user_access != 1
        with allure.step(f"Выполняем GET запрос на главную страницу приложения, проверяем получение в ответе "
                         f"статуса 401 и URL отличного от главной страницы."):
            response = self.api_client.get_main_page()
            assert response.status_code == 401
            assert response.url != self.api_client.welcome_url

    @pytest.mark.API
    def test_access_diff_f(self, setup):
        """Тест проверяет ответы приложения для ситуаций с access=2, access=1 и access=0."""
        with allure.step(f"Выставляем пользователю в БД флаг access=1, проверяем, что действие выполнилось корректно."):
            self.update_user_data(user=setup["username"], field="access", value=1)
            assert self.get_row(username=setup["username"])["access"] == 1
        with allure.step(f"Делаем GET запрос на главную страницу. Проверяем получение 200 кода и URL главной страницы"):
            response = self.api_client.get_main_page()
            assert response.status_code == 200
            assert response.url == self.api_client.welcome_url
        with allure.step(f"Выставляем пользователю в БД флаг access=0, проверяем, что действие выполнилось корректно."):
            self.update_user_data(user=setup["username"], field="access", value=0)
            assert self.get_row(username=setup["username"])["access"] == 0
        with allure.step(f"Делаем GET запрос на главную страницу. Проверяем получение 401 кода и URL, отличного от URL "
                         f"главной страницы"):
            response = self.api_client.get_main_page()
            assert response.url != self.api_client.welcome_url
            assert response.history[0].status_code == 401
