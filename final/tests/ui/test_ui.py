import pytest
from tests import base
from pages.reg_page import RegPage
from pages.main_page import MainPage
from pages.login_page import LoginPage
import allure
from datetime import datetime, timedelta


class TestRegForm(base.BaseCase):

    @pytest.mark.UI
    @pytest.mark.parametrize("param, stop", [("name", 1),
                                             ("surname", 1),
                                             ("middle_name", 0),
                                             ("username", 6),
                                             ("email", 6),
                                             ("password", 1)])
    def test_do_register_positive_f(self, param, stop, browser, delete_user_db):
        """Тест проверяет загрузку главной страницы после успешной регистрации, а также запись в БД."""
        with allure.step("Переходим на страницу регистрации, проверяем, что она открыта."):
            page = RegPage(self.browser).open()
            assert page.is_open() is True
        with allure.step("Вводим валидные данные, проверяем запись в БД и видимость элементов на главной странице."):
            page.do_register(data=self.generate_specific_user_data(param=param, stop=stop, ui_form=True))
            table = self.get_row(username=self.user_data["username"])
            assert table is not None, f"No such user: {self.user_data['username']} in database."

            assert table["name"] == self.user_data["name"], f"Wrong name in DB.\nShould be:{self.user_data['name']}\n" \
                                                            f"Got: {table['name']}"
            assert table["surname"] == self.user_data["surname"], f"Wrong surname in DB.\nShould " \
                                                                  f"be:{self.user_data['surname']}\n" \
                                                                  f"Got: {table['surname']}"
            assert table["password"] == self.user_data["password"], f"Wrong password in DB.\nShould be:" \
                                                                    f"{self.user_data['password']}\n" \
                                                                    f"Got: {table['password']}"
            assert table["email"] == self.user_data["email"], f"Wrong email in DB.\n" \
                                                              f"Should be:{self.user_data['email']}\n" \
                                                              f"Got: {table['email']}"
            assert table["access"] == 1, f"Wrong access flag in DB.\nShould be: 1\nGot: {table['access']}"
            assert MainPage(self.browser, timeout_to_open=10).is_open() is True

    @pytest.mark.UI
    def test_do_register_negative(self, browser):
        """Тест проверяет валидацию полей в форме регистрации. Пользователь не сможет зарегистрироваться, оставив
        хоть одно из обязательных к заполнению полей незаполненным. Также проверяется отсутствие записи в БД."""
        with allure.step("Переходим на страницу регистрации, проверяем, что она открыта."):
            page = RegPage(self.browser).open()
            assert page.is_open() is True
        with allure.step("Нажимаем на кнопку регистрации, не заполнив ни одного поля. "
                         "Проверяем, что остались на странице регистрации. Проверяем отсутствие записи в БД."):
            self.generate_user_data(ui_form=True)
            page.click_register()
            assert self.get_row(username=self.user_data["username"]) is None
            assert page.is_open() is True
        with allure.step("Заполняем поле Имя и нажимаем кнопку регистрации. "
                         "Проверям, что остались на той же странице. Проверяем отсутствие записи в БД."):
            page.input_name(self.user_data["name"])
            page.click_register()
            assert self.get_row(username=self.user_data["username"]) is None
            assert page.is_open() is True
        with allure.step("Заполняем поля Имя, Фамилия и нажимаем кнопку регистрации. "
                         "Проверям, что остались на той же странице. Проверяем отсутствие записи в БД."):
            page.input_name(self.user_data["name"])
            page.input_surname(self.user_data["surname"])
            page.click_register()
            assert self.get_row(username=self.user_data["username"]) is None
            assert page.is_open() is True
        with allure.step("Заполняем поля Имя, Фамилия, Логин и нажимаем кнопку регистрации. "
                         "Проверям, что остались на той же странице. Проверяем отсутствие записи в БД."):
            page.input_name(self.user_data["name"])
            page.input_surname(self.user_data["surname"])
            page.input_username(self.user_data["username"])
            page.click_register()
            assert self.get_row(username=self.user_data["username"]) is None
            assert page.is_open() is True
        with allure.step("Заполняем поля Имя, Фамилия, Логин, Почта и нажимаем кнопку регистрации. "
                         "Проверям, что остались на той же странице. Проверяем отсутствие записи в БД."):
            page.input_name(self.user_data["name"])
            page.input_surname(self.user_data["surname"])
            page.input_username(self.user_data["username"])
            page.input_email(self.user_data["email"])
            page.click_register()
            assert self.get_row(username=self.user_data["username"]) is None
            assert page.is_open() is True
        with allure.step("Заполняем поля Имя, Фамилия, Логин, Почта, Пароль и нажимаем кнопку регистрации. "
                         "Проверям, что остались на той же странице. Проверяем отсутствие записи в БД."):
            page.input_name(self.user_data["name"])
            page.input_surname(self.user_data["surname"])
            page.input_username(self.user_data["username"])
            page.input_email(self.user_data["email"])
            page.input_password(self.user_data["password"])
            page.click_register()
            assert self.get_row(username=self.user_data["username"]) is None
            assert page.is_open() is True
        with allure.step("Заполняем поля Имя, Фамилия, Логин, Почта, Пароль, нажимаем чек-бокс, далее жмем кнопку "
                         "регистрации. Проверям, что остались на той же странице. Проверяем отсутствие записи в БД."):
            page.input_name(self.user_data["name"])
            page.input_surname(self.user_data["surname"])
            page.input_username(self.user_data["username"])
            page.input_email(self.user_data["email"])
            page.input_password(self.user_data["password"])
            page.click_checkbox()
            page.click_register()
            assert self.get_row(username=self.user_data["username"]) is None
            assert page.is_open() is True
        with allure.step("Заполняем поля Имя, Фамилия, Логин, Почта, Пароль, Подтверждение пароя и нажимаем кнопку "
                         "регистрации. Проверям, что остались на той же странице, т.к. пароли не совпадают. Проверяем "
                         "отсутствие записи в БД."):
            page.input_name(self.user_data["name"])
            page.input_surname(self.user_data["surname"])
            page.input_username(self.user_data["username"])
            page.input_email(self.user_data["email"])
            page.input_password(self.user_data["password"])
            page.input_password_confirm(self.user_data["password"][:-1])
            page.click_checkbox()
            page.click_register()
            assert self.get_row(username=self.user_data["username"]) is None
            assert page.message() is True
            assert page.is_open() is True


class TestLoginForm(base.BaseCase):

    @pytest.mark.UI
    def test_do_login_f(self, setup, add_to_mock, browser):
        """Тест проверяет возможность авторизации с валидными данными, редирект на главную страницу, загрузку элементов
         главной страницы, включая VK ID, проставление start_active_time и флага active=1 в БД при авторизации и
         active=0 при деавторизации."""
        with allure.step("Переходим на страницу логина, проверяем, что она открыта."):
            page = LoginPage(self.browser).open()
            assert page.is_open() is True
        with allure.step("Авторизовываемся, проверяем загрузку главной страницы и ее элементов. Проверяем проставление "
                         "флага active=1 в БД и start_active_time."):
            page.do_login(data=setup)
            page = MainPage(self.browser)
            assert page.is_open() is True
            assert page.vk_id_is_visible() is True
            row = self.get_row(username=setup["username"])
            assert row["active"] == 1
            current_time = datetime.now().replace(second=0, microsecond=0) - timedelta(hours=3)
            assert row["start_active_time"].replace(second=0, microsecond=0) == current_time
        with allure.step("Нажимаем кнопку Logout. Проверяем загрузку страницы логина и ее элементов. Проверяем "
                         "проставление в БД флага active=0."):
            page.click_logout()
            page = LoginPage(self.browser)
            assert page.is_open() is True
            assert self.get_row(username=setup["username"])["active"] == 0
            assert self.get_row(username=setup["username"])["access"] == 0

    @pytest.mark.UI
    def test_do_login_negative(self, setup, add_to_mock, browser):
        """Тест проверяет валидацию полей на странице логина."""
        with allure.step("Переходим на страницу логина, проверяем, что она открыта."):
            page = LoginPage(self.browser).open()
            assert page.is_open() is True
        with allure.step("Жмем кнопку авторизации, проверяем, что остались на той же странице."):
            page.click_login()
            assert page.is_open() is True
        with allure.step("Вводим логин, жмем кнопку авторизации, проверяем, что остались на той же странице."):
            page.input_username(setup["username"])
            page.click_login()
            assert page.is_open() is True
        with allure.step("Вводим пароль, жмем кнопку авторизации, проверяем, что остались на той же странице."):
            page.clear_username()
            page.input_password(setup["password"])
            page.click_login()
            assert page.is_open() is True
        with allure.step("В поле логина вводим пароль, в поле пароля вводим логин, жмем кнопку авторизации, проверяем,"
                         " что остались на той же странице."):
            page.clear_password()
            page.input_username(setup["password"])
            page.input_password(setup["username"])
            page.click_login()
            assert page.message() is True
            assert page.is_open() is True


class TestMainPage(base.BaseCase):

    @pytest.mark.UI
    def test_links_f(self, setup, browser):
        """Тест проверяет наличие корректных ссылок на внешние ресурсы на главной странице, а также отсутствие на
        странице VK ID пользователя."""
        with allure.step("Переходим на страницу логина, проверяем, что она открыта."):
            page = LoginPage(self.browser).open()
            assert page.is_open() is True
        with allure.step("Авторизовываемся, проверяем загрузку главной страницы, отсутствие VK ID у пользователя и "
                         "корректность ссылок на внешние ресурсы."):
            page.do_login(data=setup)
            page = MainPage(self.browser)
            assert page.is_open() is True
            assert page.vk_id_is_visible() is False
            assert page.future_of_internet_link_correct() is True
            assert page.smtp_link_correct() is True
            assert page.news_link_correct() is True
            assert page.download_link_correct() is True
            assert page.examples_link_correct() is True
            assert page.python_link_correct() is True
            assert page.python_history_link_correct() is True
            assert page.flask_link_correct() is True
            assert page.download_centos_link_correct() is True      # leads to fedora download
            assert page.api_link_correct() is True      # incorrect

    @pytest.mark.UI
    def test_resolution(self, setup, browser):
        """Тест проверяет корректность отображения элементов при разном разрешении."""
        with allure.step("Переходим на страницу логина, проверяем, что она открыта."):
            page = LoginPage(self.browser).open()
            assert page.is_open() is True
        with allure.step("Авторизовываемся, проверяем загрузку главной страницы и отображение элементов при разном "
                         "разрешении."):
            page.do_login(data=setup)
            page = MainPage(self.browser)
            assert page.is_open() is True
            self.browser.set_window_size(width=1080, height=720)
            assert page.is_open() is True
            self.browser.set_window_size(width=800, height=600)
            assert page.is_open() is True
            self.browser.set_window_size(width=200, height=100)
            assert page.is_open() is True

    @pytest.mark.UI
    def test_access_auth_f(self, setup, browser):
        """Тест проверяет деавторизацию пользователя, при проставлении ему в БД флага access != 1."""
        with allure.step("Переходим на страницу логина, проверяем, что она открыта."):
            page = LoginPage(self.browser).open()
            assert page.is_open() is True
        with allure.step("Авторизовываемся, проверяем загрузку главной страницы."):
            page.do_login(data=setup)
            page = MainPage(self.browser)
            assert page.is_open() is True
        with allure.step("Проставляем пользователю в БД флаг access=2 и снова открываем главную страницу. Проверяем, "
                         "что открылась страница авторизации, т.к. пользователь деавторизован."):
            self.update_user_data(user=setup["username"], field="access", value=2)
            assert self.get_row(username=setup["username"])["access"] == 2
            page.open()
            page = LoginPage(self.browser).open()
            assert page.is_open() is True
