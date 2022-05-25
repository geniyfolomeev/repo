from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from faker import Faker
from ui.locators import BasePageLocators
import random


class BasePage:
    def __init__(self, browser: webdriver.Chrome):
        self.browser = browser
        self.base_locators = BasePageLocators

    def click(self, locator, timeout=5, retries=3):
        for i in range(retries):
            if i == retries - 1:
                raise TimeoutException
            try:
                WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
                WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable(locator)).click()
                break
            except TimeoutException:
                pass

    def send_keys(self, locator, text, timeout=5):
        WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
        element = WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def check_visibility(self, locator, timeout=5):
        """Проверяет видимость указанного элемента.
           Возвращает True, если элемент видно и False, если элемент не видно."""
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
            WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def return_url(self):
        return self.browser.current_url

    def move_to_element(self, locator, timeout=7):
        element = WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
        self.browser.execute_script("return arguments[0].scrollIntoView(true);", element)

    def set_mouse(self, locator, timeout=5):
        """Наводит указатель мыши на выбранный элемент."""
        WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
        element = WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(locator))
        ActionChains(self.browser).move_to_element(element).perform()

    def upload_file(self, locator, file_path, timeout=5):
        element = WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
        element.send_keys(file_path)

    def clear_field(self, locator, timeout=5):
        """Очищает выбранное поле."""
        WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
        element = WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(locator))
        element.clear()

    def generate_value(self, max_chars_count):
        faker = Faker()
        chars_count = random.randint(1, max_chars_count)
        if chars_count < 5:
            chars_count = 5
        return faker.text(chars_count).strip().replace("\n", "")

    def get_attribute_value(self, locator, attribute_name, timeout=5):
        """Возвращает значение выбранного атрибута у найденного элемента страницы."""
        WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
        element = WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(locator))
        return element.get_attribute(attribute_name)

    def get_text(self, locator, timeout=5):
        """Возвращает текст между тегами указанного элемента."""
        element = WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
        return element.text

    def page_is_loaded(self, timeout, retries_to_appear, retries_to_disappear):
        """Ждет завершения загрузки страницы, отслеживая появление и исчезновение со страницы спиннера загрузки."""
        for i in range(retries_to_appear):
            try:
                WebDriverWait(self.browser, timeout).until(
                    EC.visibility_of_element_located(self.base_locators.SPINNER))
                for j in range(retries_to_disappear):
                    try:
                        WebDriverWait(self.browser, timeout).until(
                            EC.invisibility_of_element_located(self.base_locators.SPINNER))
                        return True
                    except:
                        if j == retries_to_disappear - 1:
                            return False
                        pass
            except:
                if i == retries_to_appear - 1:
                    return True
                pass

    def click_when_loaded(self, locator, timeout_for_click=5, timeout_for_wait=3,
                          retries_spinner=2, retries_no_spinner=4):
        """Кликает на выбранный элемент после того, как со страницы исчезнет спиннер загрузки."""
        if self.page_is_loaded(timeout_for_wait, retries_spinner, retries_no_spinner):
            WebDriverWait(self.browser, timeout_for_click).until(EC.presence_of_element_located(locator))
            WebDriverWait(self.browser, timeout_for_click).until(EC.element_to_be_clickable(locator)).click()
        else:
            raise TimeoutException

    def get_elements_to_click(self, locator, number):
        """Ищет все элементы на странице по указанному локатору и кликает на элемент с указанным номером."""
        elements = self.browser.find_elements(*locator)
        if len(elements) > 1:
            elements[number].click()
        else:
            elements[0].click()

    def get_elements(self, locator) -> list:
        elements = self.browser.find_elements(*locator)
        return elements
