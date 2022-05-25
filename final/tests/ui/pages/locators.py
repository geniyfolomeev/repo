from selenium.webdriver.common.by import By


class RegPageLocators:
    REGISTRATION_TITLE = (By.XPATH, '//h3')
    NAME_FIELD = (By.XPATH, '//input[@id="user_name"]')
    SURNAME_FIELD = (By.XPATH, '//input[@id="user_surname"]')
    MIDDLE_NAME_FIELD = (By.XPATH, '//input[@id="user_middle_name"]')
    USERNAME_FIELD = (By.XPATH, '//input[@id="username"]')
    EMAIL_FIELD = (By.XPATH, '//input[@id="email"]')
    PASSWORD_FIELD = (By.XPATH, '//input[@id="password"]')
    PASSWORD_CONFIRM_FIELD = (By.XPATH, '//input[@id="confirm"]')
    ACCEPT_CHECKBOX = (By.XPATH, '//input[@id="term"]')
    REGISTER_BUTTON = (By.XPATH, '//input[@id="submit"]')
    LOG_IN_BUTTON = (By.XPATH, '//a')
    MESSAGE = (By.XPATH, '//div[@id="flash"]')


class MainPageLocators:
    MENU = (By.XPATH, '//nav[@class="uk-navbar"]')
    LOGGED_AS = (By.XPATH, '//div[@id="login-name"]/ul/li[1]')
    USER = (By.XPATH, '//div[@id="login-name"]/ul/li[2]')
    VK_ID = (By.XPATH, '//div[@id="login-name"]/ul/li[3]')
    LOGOUT_BUTTON = (By.XPATH, '//a[@class="uk-button uk-button-danger"]')
    PYTHON_FACT = (By.XPATH, '//div[@class="uk-text-center uk-text-large"]/p[1]')
    API_CIRCLE = (By.XPATH, "//div[contains(text(), 'What is an API?')]/../figure/a")
    FUTURE_INTERNET_CIRCLE = (By.XPATH, "//div[contains(text(), 'Future')]/../figure/a")
    SMTP_CIRCLE = (By.XPATH, "//div[contains(text(), 'SMTP')]/../figure/a")
    NETWORK_BUTTON = (By.XPATH, "//a[contains(text(), 'Network')]")
    LINUX_BUTTON = (By.XPATH, "//a[contains(text(), 'Linux')]")
    PYTHON_BUTTON = (By.XPATH, "//a[contains(text(), 'Python')]")
    NEWS_BUTTON = (By.XPATH, "//a[contains(text(), 'News')]")
    DOWNLOAD_BUTTON = (By.XPATH, "//a[text()='Download']")
    EXAMPLES_BUTTON = (By.XPATH, "//a[contains(text(), 'Examples')]")
    DOWNLOAD_CENTOS_BUTTON = (By.XPATH, "//a[contains(text(), 'Centos')]")
    PYTHON_HISTORY_BUTTON = (By.XPATH, "//a[contains(text(), 'history')]")
    ABOUT_FLASK_BUTTON = (By.XPATH, "//a[contains(text(), 'Flask')]")


class LoginPageLocators:
    USERNAME_FIELD = (By.XPATH, '//input[@id="username"]')
    PASSWORD_FIELD = (By.XPATH, '//input[@id="password"]')
    LOGIN_BUTTON = (By.XPATH, '//input[@id="submit"]')
    CREATE_ACCOUNT_LINK = (By.XPATH, '//a[@href="/reg"]')
    MESSAGE = (By.XPATH, '//div[@id="flash"]')
