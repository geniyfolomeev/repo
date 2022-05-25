from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, browser):
        self.browser: webdriver.Chrome = browser

    def is_visible(self, locator, timeout=10):
        """Проверяет видимость указанного элемента. Возвращает True, если элемент видно и False, если элемент
        не видно."""
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
            WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def are_visible(self, locators: list, timeout=15):
        for locator in locators:
            if not self.is_visible(locator=locator, timeout=timeout):
                raise Exception(f"Element {locator} is not visible.")

    def send_keys(self, locator, text, timeout=5):
        WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
        element = WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def click(self, locator, timeout=5, retries=3):
        for i in range(retries):
            try:
                WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
                WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable(locator)).click()
                return
            except TimeoutException:
                pass
        raise Exception(f"Could not click to element {locator[1]}")

    def url(self):
        return self.browser.current_url

    def get_attribute_value(self, locator, attribute_name, timeout=5):
        """Возвращает значение выбранного атрибута у найденного элемента страницы."""
        element = WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
        return element.get_attribute(attribute_name)

    def clear_field(self, locator, timeout=5):
        """Очищает выбранное поле."""
        WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
        element = WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(locator))
        element.clear()
