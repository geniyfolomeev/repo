from selenium.webdriver.common.by import By


class BasePageLocators:
    SPINNER = (By.CSS_SELECTOR, ".spinner")
    SEGMENTS_BUTTON = (By.XPATH, '//a[@href="/segments"]')


class LoginPageLocators(BasePageLocators):
    LOGIN_BUTTON = (By.XPATH, '//div[contains(@class, "responseHead-module-button")]')
    EMAIL_FIELD = (By.XPATH, '//input[@name="email"]')
    PASSWORD_FIELD = (By.XPATH, '//input[@name="password"]')
    LOGIN_AUTHFORM_BUTTON = (By.XPATH, '//div[contains(@class, "authForm-module-button")]')
    INVALID_LOGIN_PASSWORD_TEXT = (By.XPATH, '//div[@class="formMsg_text"]')


class DashboardPageLocators(BasePageLocators):
    CREATE_ADV_COMPANY_BUTTON = (By.XPATH, '//div[@data-test="button" and contains(@class, "button-module-blue")]')
    CAMPAIGN_NAME_TEXT = (By.XPATH, '//a[contains(@class,"nameCell-module-campaignNameLink")]')
    SELECT_ALL_CAMPAIGNS_CHECKBOX = (By.XPATH, '//input[contains(@class, "name-module-checkbox")]')
    SELECT_CAMPAIGN_CHECKBOX = (By.XPATH, '//input[contains(@class,"nameCell-module-checkbox")]')
    ACTIONS_BUTTON = (By.XPATH, '//div[contains(@class,"tableControls-module-selectItem")]')
    DELETE_BUTTON = (By.XPATH, '//li[@data-id="8"]')


class CampaignPageLocators(BasePageLocators):
    TRAFFIC_BUTTON = (By.XPATH, '//div[contains(@class, "traffic")]')
    ENTER_LINK_FIELD = (By.XPATH, '//input[contains(@class, "searchInput")]')
    BANNER_FORMAT_BUTTON = (By.XPATH, '//li[contains(@class, "banner-format")]/div')    # Формат рекламы
    BANNERS_BUTTON = (By.XPATH, '//li[contains(@class, "item-banners")]/div')   # Создание объявлений
    FORMAT_BANNER_BUTTON = (By.XPATH, '//div[contains(@id, "patterns_banner")]/span')
    FORMAT_BANNER_BUTTON_PARENT = (By.XPATH, '//div[contains(@id, "patterns_banner")]')
    LOST_AUDIENCE_TEXT = (By.XPATH, '//div[contains(@class, "slider-lost-audience-title")]') # Неохваченная аудитория
    UPLOAD_240_400_BUTTON = (By.XPATH, '//div[contains(@class, "roles-module-uploadButton") and contains(@class, "button-module-gray")]')
    UPLOAD_240_400 = (By.XPATH, '//input[@data-test="image_240x400"]')
    SAVE_AD_BUTTON = (By.XPATH, '//div[contains(@class, "button-module-blue")]')
    SAVE_CAMPAIGN_BUTTON = (By.XPATH, '//div[@class="footer__button js-save-button-wrap"]/button')
    CAMPAIGN_NAME_FIELD = (By.XPATH, '//div[@class="input input_campaign-name input_with-close"]/div[2]/input')


class SegmentsPageLocators(BasePageLocators):
    OK_VK_GROUPS_BUTTON = (By.XPATH, '//a[@href="/segments/groups_list"]')
    OK_VK_GROUPS_FIELD = (By.XPATH, '//input[contains(@class, "multiSelectSuggester-module-searchInput")]')
    OK_VK_GROUPS_SELECT_ALL_BUTTONS = (By.XPATH, '//div[contains(@class, "optionListTitle-module-control") and @data-test="select_all"]')
    OK_VK_GROUPS_ADD_TO_FAVOURITE_BUTTON = (By.XPATH, '//div[@data-test="add_selected_items_button"]/div')
    OK_VK_GROUPS_SUCCESS_TEXT = (By.XPATH, '//div[@data-class-name="SuccessView"]/div')
    OK_VK_GROUPS_TABLE_ROWS = (By.XPATH, '//tr[@class="flexi-table__row"]')
    OK_VK_GROUPS_ROWS = (By.XPATH, '//tr[@data-class-name="FlexiTableRowView"]')
    OK_VK_GROUPS_HREF = (By.XPATH, '//tr[@data-class-name="FlexiTableRowView"]/td[3]/a')
    OK_VK_GROUPS_ID = (By.XPATH, '//tr[@data-class-name="FlexiTableRowView"]/td[1]')
    OK_VK_GROUPS_LOADING = (By.XPATH, '//div[contains(@class, "multiSelectSuggester-module-pending")]')
    OK_VK_REMOVE_GROUP = (By.XPATH, '//div[@data-class-name="RemoveView"]')
    SEGMENTS_LIST_BUTTON = (By.XPATH, '//a[@href="/segments/segments_list"]')
    SEGMENTS_LIST_CREATE_BUTTON = (By.XPATH, '//a[@href="/segments/segments_list/new/"]')
    SEGMENTS_LIST_CREATE_BUTTON_NO_INSTRUCTION = (By.XPATH, '//button[@class="button button_submit"]')
    SEGMENTS_LIST_OK_VK_GROUPS_BUTTON = (By.XPATH, '//div[@class="adding-segments-item"]')
    SEGMENTS_LIST_OK_VK_GROUPS_ID = (By.XPATH, '//span[@class="adding-segments-source__src-id js-source-id"]')
    SEGMENTS_LIST_OK_VK_GROUPS_CHECKBOX = (By.XPATH, '//input[@class="adding-segments-source__checkbox js-main-source-checkbox"]')
    SEGMENTS_LIST_OK_VK_GROUPS_ADD_SEGMENT = (By.XPATH, '//div[@class="adding-segments-modal__btn-wrap js-add-button"]/button')
    SEGMENTS_LIST_CREATE_SEGMENT_FIELD = (By.XPATH, '//div[@class="input input_create-segment-form"]/div/input')
    SEGMENTS_LIST_CREATE_SEGMENT_BUTTON = (By.XPATH, '//div[contains(@class, "create-segment-form__btn-wrap js-create-segment-button-wrap")]/button')
    SEGMENTS_LIST_SEGMENT_NAME = (By.XPATH, '//div[contains(@class,"cells-module-nameCell")]/a')
    SEGMENTS_LIST_SEGMENT_ACTIONS = (By.XPATH, '//div[contains(@class,"segmentsTable-module-selectItem")]')
    SEGMENTS_LIST_SEGMENT_ACTIONS_DELETE = (By.XPATH, '//li[contains(@class,"optionsList-module-option")]')
    SEGMENTS_LIST_SEGMENTS_NAMES = (By.XPATH, '//div[contains(@class,"cells-module-nameCell")]')
    SEGMENTS_LIST_SEGMENTS_REMOVE_CHECKBOX = (By.XPATH, '//input[contains(@class,"segmentsTable-module-idCellCheckbox")]')
    REMOVE_CONFIRM = (By.XPATH, '//button[@class="button button_confirm-remove button_general"]')
    SEGMENTS_LIST_COUNT = (By.XPATH, '//a[@href="/segments/segments_list"]/span[2]')
    SEGMENTS_INSTRUCTION = (By.XPATH, '//ul[contains(@class,"instruction-module-list")]')
