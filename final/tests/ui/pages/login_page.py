import pytest
from tests.ui.pages import locators
from tests.ui.pages import base_page


class LoginPage(base_page.BasePage):
    def __init__(self, browser, timeout_to_open=15):
        base_page.BasePage.__init__(self, browser)
        self.locators = locators.LoginPageLocators
        self.url = f"{pytest.url_ui}/login"
        self.timeout_to_open = timeout_to_open

    def open(self):
        self.browser.get(self.url)
        return self

    def is_open(self):
        page_elements = [self.locators.USERNAME_FIELD, self.locators.PASSWORD_FIELD, self.locators.LOGIN_BUTTON,
                         self.locators.CREATE_ACCOUNT_LINK]
        self.are_visible(locators=page_elements, timeout=self.timeout_to_open)
        return True

    def input_username(self, text, timeout=5):
        self.send_keys(locator=self.locators.USERNAME_FIELD, text=text, timeout=timeout)

    def input_password(self, text, timeout=5):
        self.send_keys(locator=self.locators.PASSWORD_FIELD, text=text, timeout=timeout)

    def click_login(self):
        self.click(self.locators.LOGIN_BUTTON)

    def click_create_account(self):
        self.click(self.locators.CREATE_ACCOUNT_LINK)

    def do_login(self, data: dict):
        self.input_username(text=data["username"])
        self.input_password(text=data["password"])
        self.click_login()

    def clear_username(self, timeout=5):
        self.clear_field(self.locators.USERNAME_FIELD, timeout=timeout)

    def clear_password(self, timeout=5):
        self.clear_field(self.locators.PASSWORD_FIELD, timeout=timeout)

    def message(self):
        return self.is_visible(self.locators.MESSAGE)
