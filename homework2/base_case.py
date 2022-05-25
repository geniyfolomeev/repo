import os.path
import allure
import pytest
import ui.login_page
import ui.dashboard_page
from selenium.webdriver.chrome.webdriver import WebDriver
from _pytest.fixtures import FixtureRequest


class BaseCase:
    browser: WebDriver = None
    cookie = None
    is_authorized = False
    dashboard_page = None

    @pytest.fixture(autouse=True)
    def setup(self, browser):
        self.browser = browser
        if self.is_authorized:
            self.browser.get(ui.login_page.LoginPage.url)
            for cookie in self.cookie:
                self.browser.add_cookie(cookie)
            self.browser.refresh()
            return ui.dashboard_page.DashboardPage(self.browser)

    @pytest.fixture()
    def authorize_dashboard(self, setup) -> ui.dashboard_page.DashboardPage:
        if self.is_authorized:
            with allure.step("Логинимся в таргет"):
                self.dashboard_page = setup
            with allure.step("Проверяем, что попали на главную страницу"):
                assert self.dashboard_page.return_url() == self.dashboard_page.url
                assert self.dashboard_page.is_loaded() is True
                return self.dashboard_page
        else:
            with allure.step("Логинимся в таргет"):
                self.dashboard_page = ui.login_page.LoginPage(self.browser).login()
                self.cookie = self.dashboard_page.browser.get_cookies()
                self.is_authorized = True
            with allure.step("Проверяем, что попали на главную страницу"):
                assert self.dashboard_page.return_url() == self.dashboard_page.url
                assert self.dashboard_page.is_loaded(4, 2, 5) is True
                return self.dashboard_page

    @pytest.fixture(autouse=True)
    def report(self, request: FixtureRequest, temp_dir):
        failed_tests_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_tests_count:
            screenshot_path = os.path.join(temp_dir, "fail.png")
            self.browser.get_screenshot_as_file(screenshot_path)
            browser_logs = os.path.join(temp_dir, "browser.log")
            with open(browser_logs, "w") as file:
                for i in self.browser.get_log("browser"):
                    file.write(f"{i['level']} - {i['source']}\n\n{i['message']}\n\n")
            allure.attach.file(screenshot_path, "fail.png", allure.attachment_type.PNG)
            with open(browser_logs, 'r') as file:
                allure.attach(file.read(), 'test.log', allure.attachment_type.TEXT)
