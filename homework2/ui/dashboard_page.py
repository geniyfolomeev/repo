import ui.base_page
import ui.campaign_page
from ui.locators import DashboardPageLocators
from selenium.common.exceptions import TimeoutException


class DashboardPage(ui.base_page.BasePage):
    url = "https://target.my.com/dashboard"
    locators = DashboardPageLocators
    locator = DashboardPageLocators.CREATE_ADV_COMPANY_BUTTON

    def redirect_to_campaign_page(self) -> ui.campaign_page.CampaignPage:
        self.click(self.locators.CREATE_ADV_COMPANY_BUTTON)
        self.page_is_loaded(4, 1, 4)
        return ui.campaign_page.CampaignPage(self.browser)

    def get_campaign_name(self, timeout=4, retries_to_appear=4, retries_to_disappear=4, refresh=False) -> list:
        if self.page_is_loaded(timeout, retries_to_appear, retries_to_disappear):
            names = self.get_elements(self.locators.CAMPAIGN_NAME_TEXT)
            campaigns_names = [i.text for i in names]
            if refresh:
                self.browser.refresh()
                self.page_is_loaded(timeout, retries_to_appear, retries_to_disappear)
                names = self.get_elements(self.locators.CAMPAIGN_NAME_TEXT)
                campaigns_names = [i.text for i in names]
            return campaigns_names
        else:
            raise TimeoutException

    def delete_campaign(self, campaign_name):
        campaigns = self.get_elements(self.locators.CAMPAIGN_NAME_TEXT)
        for i in range(0, len(campaigns)):
            if campaigns[i].text == campaign_name:
                self.get_elements(self.locators.SELECT_CAMPAIGN_CHECKBOX)[i].click()
                break
            raise Exception(f"No such campaign: {campaign_name}")
        self.click(self.locators.ACTIONS_BUTTON)
        self.click(self.locators.DELETE_BUTTON)

    def is_loaded(self, timeout=5, retries_to_appear=2, retries_to_disappear=4):
        self.page_is_loaded(timeout=timeout, retries_to_appear=retries_to_appear, retries_to_disappear=retries_to_disappear)
        if self.check_visibility(self.locators.CREATE_ADV_COMPANY_BUTTON, timeout):
            return True
        return False
