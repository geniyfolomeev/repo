from base_case import BaseCase
import pytest


class TestMyTarget(BaseCase):

    @pytest.mark.API
    def test_create_campaign(self, api_client):
        campaign_id = self.create_campaign()
        self.delete_campaign(campaign_id)

    @pytest.mark.API
    def test_create_segment(self, api_client):
        segment_name, source_id, group_id = self.add_group()
        segment_id, source_id = self.create_segment(segment_name, source_id)
        self.delete_segment(segment_id)
        self.delete_group(group_id, source_id)

    @pytest.mark.API
    def test_delete_segment(self, api_client):
        segment_name, source_id, group_id = self.add_group(group_to_add="https://vk.com/lentach")
        segment_id, source_id = self.create_segment(segment_name, source_id)
        self.delete_segment(segment_id)
        self.delete_group(group_id, source_id)
