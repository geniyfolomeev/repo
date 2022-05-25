import campaigns
import requests


class ApiClient:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.xcsrf_token = None

    def set_cookies(self):
        """Добавляет в объект сессии куки"""
        data = {
            "email": self.email,
            "password": self.password,
            "continue": "https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email",
            "failure": "https://account.my.com/login/",
        }
        headers = {
            "Referer": "https://account.my.com/",
        }
        self.session.post("https://auth-ac.my.com//auth", data=data, headers=headers)
        self.session.get("https://target.my.com/csrf/")

        if self.session.cookies.get("csrftoken") is not None:
            self.xcsrf_token = self.session.cookies.get("csrftoken")
        else:
            raise Exception(f"No csrf token added")

    def create_campaign_traffic(self, name, price: str):
        """Создает кампанию с типом 'Трафик'"""
        data = campaigns.traffic
        data["name"] = name
        data["price"] = price

        headers = {
            "X-CSRFToken": self.xcsrf_token,
        }
        response = self.session.post("https://target.my.com/api/v2/campaigns.json", json=data, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Could not create campaign.\nResponse: {response.status_code}")
        return response

    def get_campaign(self, campaign_id, fields="id, name, status, price"):
        """Получает информацию о кампании по id"""
        params = {
            "fields": fields,
            "_id": campaign_id,
        }
        response = self.session.get("https://target.my.com/api/v2/campaigns.json", params=params)
        return response

    def delete_campaign(self, campaign_id):
        """Удаляет кампанию"""
        headers = {
            "X-CSRFToken": self.xcsrf_token,
        }
        response = self.session.delete(f"https://target.my.com/api/v2/campaigns/{campaign_id}.json", headers=headers)
        if response.status_code != 204:
            raise Exception(f"Campaign with id = {campaign_id} was not deleted.\nStatus code: {response.status_code}")
        return response

    def add_vk_group(self, group="https://vk.com/vk") -> tuple:
        """Добавляет в источники сегмента группу ВК"""
        params = {
            "_q": group,
        }
        headers = {
            "X-CSRFToken": self.xcsrf_token,
        }

        response = self.session.get("https://target.my.com/api/v2/vk_groups.json", params=params, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Could not get object_id for {group}.\nResponse: {response.status_code}")
        object_id = response.json().get("items")[0].get("id")

        if object_id is None:
            raise Exception(f"object_id is None.\nResponse: {response.json()}")

        data = {
            "object_id": object_id
        }
        response = self.session.post("https://target.my.com/api/v2/remarketing/vk_groups.json", json=data,
                                     headers=headers)
        if response.status_code != 201:
            raise Exception(f"Could not get group {group}.\nResponse: {response.status_code}")

        group_id = response.json().get("id")

        if group_id is None:
            raise Exception(f"group_id is None.\nResponse: {response.json()}")

        return object_id, group_id

    def create_segment(self, name, source_id):
        """Создает сегмент"""
        data = {
            "name": name,
            "pass_condition": 1,
            "relations": [{"object_type": "remarketing_vk_group",
                           "params": {"source_id": source_id,
                                      "type": "positive"}}],
            "logicType": "or"}
        headers = {
            "X-CSRFToken": self.xcsrf_token,
        }
        response = self.session.post("https://target.my.com/api/v2/remarketing/segments.json", json=data,
                                     headers=headers)
        if response.status_code != 200:
            raise Exception(f"Could not create segment.\nResponse: {response.status_code}")
        return response

    def get_segment(self, segment_id):
        """Получает информацию о конкретном сегменте"""
        response = self.session.get(f"https://target.my.com/api/v2/remarketing/segments/{segment_id}.json")
        return response

    def delete_segment(self, segment_id):
        """Удаляет сегмент"""
        headers = {
            "X-CSRFToken": self.xcsrf_token,
        }
        response = self.session.delete(f"https://target.my.com/api/v2/remarketing/segments/{segment_id}.json",
                                       headers=headers)
        if response.status_code != 204:
            raise Exception(f"Could not delete segment with id = {segment_id}.\nResponse: {response.status_code}")

    def get_active_groups(self):
        """Получает список активных групп ВК в источниках сегмента"""
        headers = {
            "X-CSRFToken": self.xcsrf_token,
        }
        response = self.session.get("https://target.my.com/api/v2/remarketing/vk_groups.json", headers=headers)

        if response.status_code != 200:
            raise Exception(f"Could not get VK groups info.\nResponse: {response.status_code}")

        if response.json().get("count") > 0:
            params = {
                "limit": response.json().get("count"),
            }

            response = self.session.get("https://target.my.com/api/v2/remarketing/vk_groups.json", headers=headers,
                                        params=params)
            return response
        return response

    def delete_group(self, group_id):
        """Удаляет группу ВК"""
        headers = {
            "X-CSRFToken": self.xcsrf_token,
        }
        response = self.session.delete(f"https://target.my.com/api/v2/remarketing/vk_groups/{group_id}.json",
                                       headers=headers)
        if response.status_code != 204:
            raise Exception(f"Could not delete VK group.\nResponse: {response.status_code}")
