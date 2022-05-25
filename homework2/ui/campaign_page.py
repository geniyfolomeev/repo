import os
import selenium.common.exceptions

import ui.base_page
from ui.locators import CampaignPageLocators
from ui import dashboard_page


class CampaignPage(ui.base_page.BasePage):
    url = "https://target.my.com/campaign/new"
    locators = CampaignPageLocators

    def select_traffic(self):
        self.click_when_loaded(self.locators.TRAFFIC_BUTTON)

    def enter_link(self):
        self.send_keys(self.locators.ENTER_LINK_FIELD, "https://vk.com/vk")

    def move_to_format_banner(self):
        self.set_mouse(self.locators.BANNER_FORMAT_BUTTON)
        self.click(self.locators.BANNER_FORMAT_BUTTON)

    def select_banner_format(self) -> str:
        self.move_to_element(self.locators.FORMAT_BANNER_BUTTON)
        try:
            self.page_is_loaded(4, 1, 1)
            self.click(self.locators.FORMAT_BANNER_BUTTON)
            return self.get_attribute_value(self.locators.FORMAT_BANNER_BUTTON_PARENT, "class")
        except selenium.common.exceptions.ElementClickInterceptedException:
            self.click(self.locators.FORMAT_BANNER_BUTTON_PARENT)
            return self.get_attribute_value(self.locators.FORMAT_BANNER_BUTTON_PARENT, "class")

    def move_to_banners(self):
        self.click(self.locators.BANNERS_BUTTON)

    def upload_240_400(self):
        self.set_mouse(self.locators.UPLOAD_240_400_BUTTON)
        self.upload_file(self.locators.UPLOAD_240_400, os.getcwd() + "/images/image.png")

    def save_ad(self):
        self.click(self.locators.SAVE_AD_BUTTON)

    def save_campaign(self):
        self.click(self.locators.SAVE_CAMPAIGN_BUTTON)
        self.page_is_loaded(4, 2, 2)
        return dashboard_page.DashboardPage(self.browser)

    def set_campaign_name(self):
        self.move_to_element(self.locators.CAMPAIGN_NAME_FIELD)
        self.clear_field(self.locators.CAMPAIGN_NAME_FIELD, timeout=8)
        data = self.generate_value(max_chars_count=255)
        self.send_keys(self.locators.CAMPAIGN_NAME_FIELD, data)
        return data

    def create_traffic_campaign(self):
        self.select_traffic()
        self.enter_link()
        campaign_name = self.set_campaign_name()
        self.move_to_format_banner()
        self.select_banner_format()
        self.move_to_banners()
        self.upload_240_400()
        self.save_ad()
        page = self.save_campaign()
        return page, campaign_name

    def is_loaded(self, timeout=5, retries_to_appear=2, retries_to_disappear=4):
        self.page_is_loaded(timeout=timeout, retries_to_appear=retries_to_appear, retries_to_disappear=retries_to_disappear)
        if self.check_visibility(self.locators.TRAFFIC_BUTTON, timeout):
            return True
