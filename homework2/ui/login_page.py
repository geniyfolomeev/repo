from ui.creds import log, pas
import ui.base_page
from ui.locators import LoginPageLocators
import ui.dashboard_page


class LoginPage(ui.base_page.BasePage):
    url = 'https://target.my.com/'
    locators = LoginPageLocators

    def login(self, login=log, password=pas):
        self.browser.get(self.url)
        self.click_when_loaded(self.locators.LOGIN_BUTTON, timeout_for_wait=5, retries_spinner=2, retries_no_spinner=7)
        self.send_keys(self.locators.EMAIL_FIELD, login)
        self.send_keys(self.locators.PASSWORD_FIELD, password)
        self.click(self.locators.LOGIN_AUTHFORM_BUTTON)
        self.page_is_loaded(4, 1, 4)
        return ui.dashboard_page.DashboardPage(browser=self.browser)
