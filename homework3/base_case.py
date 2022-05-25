import random

import pytest


class BaseCase:
    @pytest.fixture(autouse=True)
    def setup(self, api_client):
        self.api_client = api_client

    def add_group(self, group_to_add="https://vk.com/vk") -> tuple:
        segment_name = self.generate_value(range_start=1, range_finish=60)  # Generating test data

        source_id, group_id = self.api_client.add_vk_group(group=group_to_add)  # Getting VK group id`s
        groups = self.api_client.get_active_groups().json().get("items")  # Getting active groups info
        groups_id = [i["object_id"] for i in groups]  # Getting active groups id`s

        assert source_id in groups_id, f"VK group with id = {source_id} has not created"

        return segment_name, source_id, group_id

    def create_segment(self, segment_name, source_id) -> tuple:
        segment_id = self.api_client.create_segment(name=segment_name,  # Getting created segment id
                                                    source_id=source_id).json().get("id")

        segment_info = self.api_client.get_segment(segment_id=segment_id).json()  # Getting segment info

        assert segment_info.get("id") == segment_id
        assert segment_info.get("name") == segment_name

        return segment_id, source_id

    def delete_segment(self, segment_id):
        self.api_client.delete_segment(segment_id)  # Deleting segment
        response = self.api_client.get_segment(segment_id=segment_id)

        assert response.status_code == 404

    def delete_group(self, group_id, source_id):
        self.api_client.delete_group(group_id)  # Deleting group
        groups = self.api_client.get_active_groups().json().get("items")  # Getting active groups info
        groups_id = [i["object_id"] for i in groups]  # Getting active groups id`s

        assert source_id not in groups_id, f"VK Group with id = {source_id} was not deleted"

    def create_campaign(self):
        campaign_name = self.generate_value(range_start=1, range_finish=255)  # Generating test data
        price = self.generate_value(range_start=1, range_finish=7, price_mode=True)

        campaign_id = self.api_client.create_campaign_traffic(campaign_name, price).json().get("id")  # Creating
        # traffic type campaign
        campaign_info = self.api_client.get_campaign(campaign_id=campaign_id).json().get("items")[0]  # Getting
        # campaign info

        assert campaign_info.get("id") == campaign_id
        assert campaign_info.get("name") == campaign_name
        assert campaign_info.get("price") == price
        assert campaign_info.get("status") == 'active'

        return campaign_id

    def delete_campaign(self, campaign_id):
        self.api_client.delete_campaign(campaign_id)  # Deleting campaign
        campaign_info = self.api_client.get_campaign(campaign_id=campaign_id).json()  # Getting campaign info

        assert campaign_info.get("items")[0].get("status") == 'deleted'

    def generate_value(self, range_start, range_finish, price_mode=False):
        data = "АБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ абвгдеёжзиклмнопрстуфхцчшщъыьэюя"
        length = random.randint(range_start, range_finish)  # Generates random input`s length
        value = ""

        if price_mode:
            # max price = 500, min price = 0.01
            numbers = "1234567890"
            boundary = ("0.01", "0.02", "0.03", "0.10", "1.00", "499.00", "499.10", "499.30", "500.00")
            length = random.randint(range_start, range_finish)
            if length == 1:
                value = random.choice(numbers[:-1]) + ".00"
                return value
            elif length == 2:
                value += random.choice(numbers[:-1])
                value = value + random.choice(numbers) + ".00"
                return value
            elif length == 3:
                flip = random.choice([True, False])
                if flip:
                    value = random.choice(numbers) + "." + random.choice(numbers) + "0"
                    return value
                else:
                    value = random.choice(numbers[:-1]) + random.choice(numbers) + random.choice(numbers) + ".00"
                    if int(float(value)) > 500:
                        value = random.choice(boundary)
                    return value
            else:
                value = random.choice(boundary)
                return value

        for i in range(length):
            value += random.choice(data)

        return value.strip()
