import pytest
from tests.ui.pages import locators
from tests.ui.pages import base_page


class RegPage(base_page.BasePage):
    def __init__(self, browser, timeout_to_open=15):
        base_page.BasePage.__init__(self, browser)
        self.locators = locators.RegPageLocators
        self.url = f"{pytest.url_ui}/reg"
        self.timeout_to_open = timeout_to_open

    def open(self):
        self.browser.get(self.url)
        return self

    def is_open(self):
        page_elements = [self.locators.REGISTRATION_TITLE, self.locators.NAME_FIELD, self.locators.SURNAME_FIELD,
                         self.locators.MIDDLE_NAME_FIELD, self.locators.USERNAME_FIELD, self.locators.EMAIL_FIELD,
                         self.locators.PASSWORD_FIELD, self.locators.PASSWORD_CONFIRM_FIELD,
                         self.locators.ACCEPT_CHECKBOX, self.locators.REGISTER_BUTTON]
        self.are_visible(locators=page_elements, timeout=self.timeout_to_open)
        return True

    def input_name(self, text, timeout=5):
        self.send_keys(locator=self.locators.NAME_FIELD, text=text, timeout=timeout)

    def message(self):
        return self.is_visible(self.locators.MESSAGE)

    def input_surname(self, text, timeout=5):
        self.send_keys(locator=self.locators.SURNAME_FIELD, text=text, timeout=timeout)

    def input_middle_name(self, text, timeout=5):
        self.send_keys(locator=self.locators.MIDDLE_NAME_FIELD, text=text, timeout=timeout)

    def input_username(self, text, timeout=5):
        self.send_keys(locator=self.locators.USERNAME_FIELD, text=text, timeout=timeout)

    def input_email(self, text, timeout=5):
        self.send_keys(locator=self.locators.EMAIL_FIELD, text=text, timeout=timeout)

    def input_password(self, text, timeout=5):
        self.send_keys(locator=self.locators.PASSWORD_FIELD, text=text, timeout=timeout)

    def input_password_confirm(self, text, timeout=5):
        self.send_keys(locator=self.locators.PASSWORD_CONFIRM_FIELD, text=text, timeout=timeout)

    def click_checkbox(self):
        self.click(locator=self.locators.ACCEPT_CHECKBOX)

    def click_register(self):
        self.click(locator=self.locators.REGISTER_BUTTON)

    def do_register(self, data: dict):
        self.input_name(text=data["name"])
        self.input_surname(text=data["surname"])
        self.input_middle_name(text=data["middle_name"])
        self.input_username(text=data["username"])
        self.input_email(text=data["email"])
        self.input_password(text=data["password"])
        self.input_password_confirm(text=data["password"])
        self.click_checkbox()
        self.click_register()
