from tests.ui.pages import base_page
from tests.ui.pages import locators
import pytest


class MainPage(base_page.BasePage):
    def __init__(self, browser, timeout_to_open=15):
        base_page.BasePage.__init__(self, browser)
        self.locators = locators.MainPageLocators
        self.url = f"{pytest.url_ui}/welcome/"
        self.timeout_to_open = timeout_to_open

    def open(self):
        self.browser.get(self.url)
        return self

    def is_open(self):
        page_elements = [self.locators.MENU, self.locators.LOGOUT_BUTTON, self.locators.USER, self.locators.LOGGED_AS,
                         self.locators.PYTHON_FACT]
        self.are_visible(locators=page_elements, timeout=self.timeout_to_open)
        return True

    def vk_id_is_visible(self):
        return self.is_visible(self.locators.VK_ID)

    def click_logout(self):
        self.click(self.locators.LOGOUT_BUTTON)

    def api_link_correct(self):
        link = self.get_attribute_value(locator=self.locators.API_CIRCLE, attribute_name="href")
        if link == "https://en.wikipedia.org/wiki/API":
            return True
        return f"Should be: 'https://en.wikipedia.org/wiki/API', got: {link}"

    def future_of_internet_link_correct(self):
        link = self.get_attribute_value(locator=self.locators.FUTURE_INTERNET_CIRCLE, attribute_name="href")
        if link == "https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/":
            return True
        return False

    def smtp_link_correct(self):
        link = self.get_attribute_value(locator=self.locators.SMTP_CIRCLE, attribute_name="href")
        if link == "https://ru.wikipedia.org/wiki/SMTP":
            return True
        return False

    def news_link_correct(self):
        link = self.get_attribute_value(locator=self.locators.NEWS_BUTTON, attribute_name="href")
        if link == "https://www.wireshark.org/news/":
            return True
        return False

    def download_link_correct(self):
        link = self.get_attribute_value(locator=self.locators.DOWNLOAD_BUTTON, attribute_name="href")
        if link == "https://www.wireshark.org/#download":
            return True
        return f"Should be: 'https://www.wireshark.org/#download', got: {link}"

    def examples_link_correct(self):
        link = self.get_attribute_value(locator=self.locators.EXAMPLES_BUTTON, attribute_name="href")
        if link == "https://hackertarget.com/tcpdump-examples/":
            return True
        return False

    def download_centos_link_correct(self):
        link = self.get_attribute_value(locator=self.locators.DOWNLOAD_CENTOS_BUTTON, attribute_name="href")
        if link == "https://www.centos.org/download/":
            return True
        return f"Should be: 'https://www.centos.org/download/', got: {link}"

    def python_link_correct(self):
        link = self.get_attribute_value(locator=self.locators.PYTHON_BUTTON, attribute_name="href")
        if link == "https://www.python.org/":
            return True
        return False

    def python_history_link_correct(self):
        link = self.get_attribute_value(locator=self.locators.PYTHON_HISTORY_BUTTON, attribute_name="href")
        if link == "https://en.wikipedia.org/wiki/History_of_Python":
            return True
        return False

    def flask_link_correct(self):
        link = self.get_attribute_value(locator=self.locators.ABOUT_FLASK_BUTTON, attribute_name="href")
        if link == "https://flask.palletsprojects.com/en/1.1.x/#":
            return True
        return False
