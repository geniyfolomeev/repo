from datetime import datetime, timedelta
import random
import pytest
from database.client import MysqlClient
from api.client import ApiClient
import allure
import docker
from docker.models.containers import Container
from pytest import FixtureRequest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class BaseCase:
    mysql_client: MysqlClient = MysqlClient(db_name='vkeducation', user='root', password='pass')
    api_client: ApiClient = ApiClient()
    docker_client = docker.from_env()
    url = pytest.url
    auth_user_data = None
    user_data = None
    browser = None
    vk_id = None

    @pytest.fixture(scope="session")
    def setup(self):
        """Создает пользователя в БД, от лица которого будет авторизован API клиент. Авторизовывает API клиент.
        По завершении теста удаляет из БД созданного ранее пользователя."""
        with allure.step("Добавляем пользователя для авторизации в БД."):
            self.mysql_client.connect()
            self.mysql_client.insert_data(user_data=self.generate_user_data(auth=True, ui_form=True))
        with allure.step("Авторизовываемся от лица добавленного пользователя. "
                         "Проверяем ответ приложения при авторизации, а также URL после редиректа."):
            response = self.api_client.authorize(user_data=self.auth_user_data)

            assert response.status_code == 200, f"Authorization unsuccessful"
            assert response.url == f"{pytest.url}/welcome/", f"Authorization unsuccessful"
        yield self.auth_user_data
        with allure.step("Удаляем из базы добавленного ранее пользователя."):
            self.mysql_client.connect()
            self.mysql_client.delete_by_username(username=self.auth_user_data["username"])
            self.mysql_client.connection.close()

    @pytest.fixture(scope="function")
    def delete_user_db(self):
        """По окончании теста удаляет из БД пользователя, с логином, записанным в self.user_data."""
        yield
        self.mysql_client.connect()
        self.mysql_client.delete_by_username(username=self.user_data["username"])

    def generate_value(self, stop: int,
                       start=0,
                       email=False,
                       random_length=True) -> str:
        """Генерирует случайную последовательность согласно указанному в параметрах формату.

        :param stop: int - максимальная длина генерируемой последовательности.
        :param email: bool - режим генерации данных для электронной почты, если True.
        :param start: int - минимальная длина генерируемой последовательности для random_length=True.
        :param random_length: bool - случайная длина последовательности, от start до stop, если True. Если же False, то
        генерируется последовательность максимальной длины."""

        chars = r'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if email:
            if stop > 56:
                stop = 56
            if stop < 6:
                stop = 6
            stop = random.randint(start, stop) if random_length else stop
            return ("".join(random.choice(chars) for i in range(0, stop))).strip() + "@mail.ru"
        stop = random.randint(start, stop) if random_length else stop
        return ("".join(random.choice(chars) for i in range(0, stop))).strip()

    def generate_user_data(self, add_middle_name=True, random_length=True, correct_validation=True, auth=False,
                           ui_form=False) -> dict:
        """Генерирует данные для создания пользователя.

        :param add_middle_name: bool - наличие у пользователя отчества, если True.
        :param random_length: bool - случайная длина строки, если True, иначе максимальная длина строки.
        :param correct_validation: bool - размер строки не превышает выделенного для нее места в БД, если True.
        :param auth: bool - генерация данных для авторизации, если True.
        :param ui_form: bool - генерирует данные для заполнения UI формы регистрации, если True. Если False, то
        генерирует данные для создания пользователя по API."""

        user_data = {
            "name": self.generate_value(start=1, stop=45,
                                        random_length=random_length),
            "surname": self.generate_value(start=1, stop=300,
                                           random_length=random_length),
            "middle_name": self.generate_value(stop=300,
                                               random_length=random_length) if add_middle_name else None,
            "username": self.generate_value(start=6,
                                            stop=16,
                                            random_length=random_length),
            "email": self.generate_value(start=6, stop=64, email=True, random_length=random_length),
            "password": self.generate_value(start=6,
                                            stop=255,
                                            random_length=random_length),
        }
        if correct_validation:
            user_data["middle_name"] = self.generate_value(stop=255,
                                                           random_length=random_length) if add_middle_name else None
            user_data["surname"] = self.generate_value(start=1, stop=255, random_length=random_length)
            user_data["email"] = self.generate_value(start=6,
                                                     stop=64, email=True, random_length=random_length)
        if ui_form:
            user_data["surname"] = self.generate_value(start=1, stop=255,
                                                       random_length=random_length)
            user_data["middle_name"] = self.generate_value(stop=255,
                                                           random_length=random_length) if add_middle_name else None
            if correct_validation:
                user_data = {
                    "name": self.generate_value(start=1, stop=20,
                                                random_length=random_length),
                    "surname": self.generate_value(start=1, stop=20,
                                                   random_length=random_length),
                    "middle_name": self.generate_value(stop=20,
                                                       random_length=random_length) if add_middle_name else None,
                    "username": self.generate_value(start=6,
                                                    stop=16,
                                                    random_length=random_length),
                    "email": self.generate_value(start=6, stop=64, email=True, random_length=random_length),
                    "password": self.generate_value(start=6,
                                                    stop=50,
                                                    random_length=random_length),
                }

        if auth:
            self.auth_user_data = user_data
        else:
            self.user_data = user_data

        return user_data

    def get_row(self, username: str):
        """Получает информацию о пользователе из БД по его логину.

        :param username: str - логин пользователя"""
        try:
            return self.mysql_client.get_row_by_username(username)[0]
        except IndexError:
            return None

    @pytest.fixture(scope="function", autouse=True)
    def report(self, request: FixtureRequest):
        """Пишет лог приложения в момент выполнения теста."""
        failed_tests_count = request.session.testsfailed
        start_date_time = datetime.now() - timedelta(hours=3)
        app_container: Container = self.docker_client.containers.list(filters={"name": "app"})[0]
        yield
        if request.session.testsfailed > failed_tests_count:
            finish_date_time = datetime.now() - timedelta(hours=2, minutes=59, seconds=59)
            with open(f"api/logs/app_logs_{request.node.name}.log", "w") as file:
                for line in app_container.logs(stream=True, since=start_date_time, until=finish_date_time,
                                               follow=False):
                    file.write(f'{line.decode("utf-8").strip()}\n')
            with open(f"api/logs/app_logs_{request.node.name}.log", 'r') as file:
                allure.attach(file.read(), 'app_log.log', allure.attachment_type.TEXT)

    @pytest.fixture(scope="function")
    def browser(self, request):
        selenoid = request.config.getoption('--selenoid')
        if selenoid:
            pytest.url_ui = "http://app:8080"
            options = webdriver.ChromeOptions()
            self.browser = webdriver.Remote("http://localhost:4444/wd/hub", options=options)
        else:
            self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        self.browser.maximize_window()
        failed_tests_count = request.session.testsfailed
        yield
        pytest.url_ui = "http://127.0.0.1:8080"
        if request.session.testsfailed > failed_tests_count:
            self.browser.get_screenshot_as_file(f"ui/screenshots/{request.node.name}.png")
            with open(f"ui/logs/{request.node.name}.log", "w") as file:
                for i in self.browser.get_log("browser"):
                    file.write(f"{i['level']} - {i['source']}\n\n{i['message']}\n\n")
            allure.attach.file(f"ui/screenshots/{request.node.name}.png", "fail.png", allure.attachment_type.PNG)
            with open(f"ui/logs/{request.node.name}.log", 'r') as file:
                allure.attach(file.read(), 'browser.log', allure.attachment_type.TEXT)
        self.browser.quit()

    def generate_specific_user_data(self, param, stop, ui_form=False, correct_validation=False):
        self.generate_user_data(ui_form=ui_form, random_length=False, correct_validation=correct_validation)
        if param == "email":
            self.user_data[param] = self.generate_value(stop=stop, random_length=False, email=True)
        elif param == "password":
            self.user_data[param] = self.generate_value(stop=stop, random_length=False)
            self.user_data["password_confirm"] = self.user_data[param]
        else:
            self.user_data[param] = self.generate_value(stop=stop, random_length=False)

        return self.user_data

    @pytest.fixture(scope="function")
    def add_to_mock(self, setup):
        """Генерирует данные пользователя, а также добавляет пользователя в БД мока. По завершении теста
         удаляет пользователя из БД мока."""
        self.vk_id = random.randint(0, 999999999)
        response = self.api_client.post_user_mock(username=setup["username"], user_id=self.vk_id)
        yield response
        self.api_client.delete_user_mock(username=setup["username"])

    def update_user_data(self, field: str, value, user: str):
        data = {
            field: value
        }
        self.mysql_client.update_user_data(username=user, user_data=data)
