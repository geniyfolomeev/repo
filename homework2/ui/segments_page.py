import ui.base_page
from ui.locators import SegmentsPageLocators
import selenium.common.exceptions


class NoLinkException(BaseException):
    pass


class NoSuchSourceException(BaseException):
    pass


class SegmentsPage(ui.base_page.BasePage):
    url = 'https://target.my.com/segments/segments_list'
    locators = SegmentsPageLocators

    def open(self):
        self.browser.get(self.url)
        return SegmentsPage(self.browser)

    def move_to_vk_ok(self):
        """Переход на вкладку 'Группы OK и VK'"""
        if self.page_is_loaded(5, 2, 7):
            self.click(self.locators.OK_VK_GROUPS_BUTTON, timeout=6, retries=5)
        else:
            self.browser.refresh()
            self.page_is_loaded(5, 2, 7)
            self.click(self.locators.OK_VK_GROUPS_BUTTON, timeout=6, retries=5)

    def add_group(self, group_to_add, range_candy_bar_appear=100, range_candy_bar_disappear=100, range_new_string=100) -> tuple:
        self.page_is_loaded(3, 3, 3)
        if group_to_add not in self.browser.page_source:
            link_elements_before_add = self.get_elements(self.locators.OK_VK_GROUPS_HREF)
        else:
            link_elements_before_add = []
        self.send_keys(self.locators.OK_VK_GROUPS_FIELD, group_to_add, timeout=10)
        for i in range(range_candy_bar_appear):
            try:
                self.browser.find_element(*self.locators.OK_VK_GROUPS_LOADING)  # Проверяем, что плашка загрузки догрузилась
                for j in range(range_candy_bar_disappear):
                    loading = self.browser.find_elements(*self.locators.OK_VK_GROUPS_LOADING)
                    if len(loading) == 0:
                        break
                    if j == range_candy_bar_disappear - 1:
                        raise selenium.common.exceptions.TimeoutException
                break
            except:
                if i == range_candy_bar_appear - 1:
                    raise selenium.common.exceptions.TimeoutException
                pass
        self.get_elements_to_click(self.locators.OK_VK_GROUPS_SELECT_ALL_BUTTONS, 1)
        self.click(self.locators.OK_VK_GROUPS_ADD_TO_FAVOURITE_BUTTON)
        for i in range(range_new_string):
            link_elements = self.get_elements(self.locators.OK_VK_GROUPS_HREF)
            if len(link_elements) > len(link_elements_before_add):
                links = [i.get_attribute("href") for i in link_elements]
                for j in range(0, len(links)):
                    if links[j] == group_to_add:
                        id_elements = self.get_elements(self.locators.OK_VK_GROUPS_ID)
                        group_id = [o.text for o in id_elements][j]
                        return links, group_id
            if i == range_new_string - 1:
                raise Exception("New group has not added")

    def move_to_segments_list(self):
        self.click(self.locators.SEGMENTS_LIST_BUTTON)

    def create_segment(self, group_id) -> str:
        segment_name = self.generate_value(max_chars_count=60)
        if self.check_visibility(self.locators.SEGMENTS_INSTRUCTION):
            self.click(self.locators.SEGMENTS_LIST_CREATE_BUTTON)
        else:
            self.click(self.locators.SEGMENTS_LIST_CREATE_BUTTON_NO_INSTRUCTION)

        self.get_elements_to_click(self.locators.SEGMENTS_LIST_OK_VK_GROUPS_BUTTON, 1)
        groups_elements = self.get_elements(self.locators.SEGMENTS_LIST_OK_VK_GROUPS_ID)
        groups_id = [i.text[1:] for i in groups_elements]
        for i in range(0, len(groups_id)):
            if groups_id[i] == group_id:
                self.get_elements(self.locators.SEGMENTS_LIST_OK_VK_GROUPS_CHECKBOX)[i].click()
        self.click(self.locators.SEGMENTS_LIST_OK_VK_GROUPS_ADD_SEGMENT)
        self.send_keys(self.locators.SEGMENTS_LIST_CREATE_SEGMENT_FIELD, segment_name)
        self.click(self.locators.SEGMENTS_LIST_CREATE_SEGMENT_BUTTON)
        self.page_is_loaded(4, 2, 4)
        return segment_name

    def get_segments_names(self, range_to_get_segments=100) -> list:
        for i in range(0, range_to_get_segments):
            segments_names_elements = self.get_elements(self.locators.SEGMENTS_LIST_SEGMENT_NAME)
            if len(segments_names_elements) == 0:
                pass
            else:
                return [i.text for i in segments_names_elements]

    def remove_segment(self, segment_name, timeout=8):
        segments_names_elements = self.get_elements(self.locators.SEGMENTS_LIST_SEGMENTS_NAMES)
        segments_names = [i.text for i in segments_names_elements]
        for i in range(0, len(segments_names)):
            if segments_names[i] == segment_name:
                self.get_elements_to_click(self.locators.SEGMENTS_LIST_SEGMENTS_REMOVE_CHECKBOX, i + 1)
                self.click(self.locators.SEGMENTS_LIST_SEGMENT_ACTIONS, timeout=timeout)
                self.click(self.locators.SEGMENTS_LIST_SEGMENT_ACTIONS_DELETE, timeout=timeout)
                return True
        raise Exception("No such segment name")

    def remove_ok_vk_group(self, group_id):
        groups_id_elements = self.get_elements(self.locators.OK_VK_GROUPS_ID)
        groups_id = [i.text for i in groups_id_elements]
        for i in range(0, len(groups_id)):
            if groups_id[i] == group_id:
                self.get_elements_to_click(self.locators.OK_VK_REMOVE_GROUP, i)
                self.click(self.locators.REMOVE_CONFIRM)
                self.page_is_loaded(4, 1, 1)
                return True
        raise Exception(f"No such group id:{group_id} in groups list")

    def get_ok_vk_groups_id(self, range_to_get_groups=100) -> list:
        self.browser.refresh()
        self.page_is_loaded(4, 1, 2)
        for i in range(0, range_to_get_groups):
            groups_id_elements = self.get_elements(self.locators.OK_VK_GROUPS_ID)
            if len(groups_id_elements) == 0:
                pass
            return [i.text for i in groups_id_elements]

    def is_loaded(self, timeout=5, retries_to_appear=2, retries_to_disappear=4):
        self.page_is_loaded(timeout=timeout, retries_to_appear=retries_to_appear, retries_to_disappear=retries_to_disappear)
        if self.check_visibility(self.locators.SEGMENTS_LIST_BUTTON, timeout):
            return True
