import pytest
from base import BaseCase
import locators


class TestMyTarget(BaseCase):
    @pytest.mark.UI
    def test_login(self):
        self.browser.get("https://target.my.com/")
        self.login()
        self.wait(2)  # Для надежности
        assert self.browser.current_url == 'https://target.my.com/dashboard'

    @pytest.mark.UI
    def test_logout(self):
        self.browser.get("https://target.my.com/dashboard")
        self.login()
        self.wait(2)  # Для надежности
        assert self.browser.current_url == 'https://target.my.com/dashboard'
        self.click_when_loaded(locators.RIGHT_MODULE_BUTTON)
        self.click(locators.RIGHT_MODULE_LOGOUT_BUTTON)
        self.wait(2)
        assert self.browser.current_url == 'https://target.my.com/'

    @pytest.mark.UI
    def test_contact_info(self):
        fio = self.generate_value(0, 100, False)
        phone = self.generate_value(0, 20, True)
        url = 'https://target.my.com/profile/contacts'
        self.browser.get(url)
        self.login()
        self.wait(2)  # Для надежности
        assert self.browser.current_url == url
        self.clear_field(locators.FIO_FIELD)  # Очищаем поле ФИО
        self.send_keys(locators.FIO_FIELD, fio)
        self.clear_field(locators.PHONE_FIELD)  # Очищаем поле Контактный телефон
        self.send_keys(locators.PHONE_FIELD, phone)
        self.click(locators.SAVE_BUTTON)
        assert self.check_visibility(locators.SUCCESS_TEXT) is True  # Должна появиться плашка "Информация сохранена"
        self.browser.refresh()
        self.wait(5)
        assert fio == self.attribute_value(locators.FIO_FIELD, "value")  # Валидация ФИО
        assert phone == self.attribute_value(locators.PHONE_FIELD, "value")  # Валидация номера телефона

    @pytest.mark.UI
    @pytest.mark.parametrize("locator, valid_url",
                             [(locators.AUDIT_SEGM_BUTTON, "https://target.my.com/segments"),
                              (locators.STATISTICS_BUTTON, "https://target.my.com/statistics")])
    def test_change_page(self, locator, valid_url):
        self.browser.get("https://target.my.com/")
        self.login()
        self.wait(2)  # Для надежности
        assert self.browser.current_url == 'https://target.my.com/dashboard'
        self.click_long(locator)
        self.wait(1)
        assert self.browser.current_url == valid_url
