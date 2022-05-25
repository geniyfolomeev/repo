import allure
import pytest
from base_case import BaseCase
import ui.login_page
import ui.segments_page


class TestMyTarget(BaseCase):
    @pytest.mark.parametrize("incorrect_login, incorrect_password",
                             [pytest.param("3!daFsE37mq63AJ", "geniyfolomeev@gmail.com"),
                              pytest.param("123", "321")])
    @pytest.mark.UI
    def test_login_negative(self, incorrect_login, incorrect_password):
        login_page = ui.login_page.LoginPage(self.browser)
        with allure.step("Вбиваем некорректный логин и пароль в таргете"):
            page = login_page.login(incorrect_login, incorrect_password)
        with allure.step("Проверяем, что мы не попали на главную страницу таргета"):
            assert page.return_url() != "https://target.my.com/dashboard"
            assert page.is_loaded(2, 1, 1) is False

    @pytest.mark.UI
    def test_create_adv_campaign(self, authorize_dashboard):
        with allure.step("Переходим на страницу создания рекламной кампании"):
            page = authorize_dashboard
            page = page.redirect_to_campaign_page()
        with allure.step("Проверяем, что открылась страница создания рекламной кампании"):
            assert page.return_url() == page.url
            assert page.is_loaded(5, 2, 7) is True
        with allure.step("Создаем рекламную кампанию"):
            page, campaign_name = page.create_traffic_campaign()
        with allure.step("Проверяем, что создалась кампания с указанным ранее названием"):
            assert campaign_name in page.get_campaign_name(5, 2, 6)
        with allure.step("Удаляем созданную кампанию"):
            page.delete_campaign(campaign_name)
        with allure.step("Проверяем, что созданная ранее кампания удалилась"):
            assert campaign_name not in page.get_campaign_name(refresh=True)

    @pytest.mark.UI
    def test_create_segment(self, authorize_dashboard):
        group_to_add = "https://vk.com/vk"
        with allure.step("Переходим на страницу создания сегмента"):
            page = ui.segments_page.SegmentsPage(self.browser).open()
        with allure.step("Проверяем, что открылась страница создания сегмента"):
            assert page.is_loaded(5, 2, 5) is True
        with allure.step("Переходим на вкладку 'Группы ОК и VK'"):
            page.move_to_vk_ok()
        with allure.step("Добавляем группу ВК"):
            groups, group_id = page.add_group(group_to_add)
        with allure.step("Проверяем, что список групп не пуст и в нем присутствует добавленная ранее группа"):
            assert len(groups) > 0
            assert group_to_add in groups
        with allure.step("Переходим на вкладку 'Список сегментов'"):
            page.move_to_segments_list()
        with allure.step("Создаем сегмент с источником в виде группы, созданной ранее"):
            segment_name = page.create_segment(group_id)
        with allure.step("Получаем список действующих сегментов и проверяем наличие созданного ранее сегмента в этом "
                         "списке"):
            active_segments = page.get_segments_names()
            assert len(active_segments) > 0
            assert segment_name in active_segments
        with allure.step("Удаляем созданный ранее сегмент"):
            page.remove_segment(segment_name)
        with allure.step("Получаем список действующих сегментов и проверяем наличие созданного ранее сегмента в этом "
                         "списке"):
            active_segments = page.get_segments_names()
            assert segment_name not in active_segments
        with allure.step("Переходим на вкладку 'Группы ОК и VK'"):
            page.move_to_vk_ok()
        with allure.step("Удаляем созданную ранее группу ВК"):
            page.remove_ok_vk_group(group_id)
        with allure.step("Получаем список активных групп ОК и VK, проверяем отсутствие в этом списке удаленной ранее "
                         "группы"):
            active_groups = page.get_ok_vk_groups_id()
            assert group_id not in active_groups

    @pytest.mark.UI
    def test_delete_segment(self, authorize_dashboard):
        group_to_add = "https://vk.com/lentach"
        with allure.step("Переходим на страницу создания сегмента"):
            page = ui.segments_page.SegmentsPage(self.browser).open()
        with allure.step("Проверяем, что открылась страница создания сегмента"):
            assert page.is_loaded(5, 2, 5) is True
        with allure.step("Переходим на вкладку 'Группы ОК и VK'"):
            page.move_to_vk_ok()
        with allure.step("Добавляем группу ВК"):
            groups, group_id = page.add_group(group_to_add)
        with allure.step("Проверяем, что список групп не пуст и в нем присутствует добавленная ранее группа"):
            assert len(groups) > 0
            assert group_to_add in groups
        with allure.step("Переходим на вкладку 'Список сегментов'"):
            page.move_to_segments_list()
        with allure.step("Создаем сегмент с источником в виде группы, созданной ранее"):
            segment_name = page.create_segment(group_id)
        with allure.step(
                "Получаем список действующих сегментов и проверяем наличие созданного ранее сегмента в этом списке"):
            active_segments = page.get_segments_names()
            assert len(active_segments) > 0
            assert segment_name in active_segments
        with allure.step("Удаляем созданный ранее сегмент"):
            page.remove_segment(segment_name)
        with allure.step(
                "Получаем список действующих сегментов и проверяем наличие созданного ранее сегмента в этом списке"):
            active_segments = page.get_segments_names()
            assert segment_name not in active_segments
        with allure.step("Переходим на вкладку 'Группы ОК и VK'"):
            page.move_to_vk_ok()
        with allure.step("Удаляем созданную ранее группу ВК"):
            page.remove_ok_vk_group(group_id)
        with allure.step(
                "Получаем список активных групп ОК и VK, проверяем отсутствие в этом списке удаленной ранее группы"):
            active_groups = page.get_ok_vk_groups_id()
            assert group_id not in active_groups
