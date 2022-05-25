from models import RequestsModel, RequestsTypeModel, TopRequestsModel, BiggestClientErrModel, BiggestServerErrModel
from log_parser import parse_log


class MysqlBuilder:

    def __init__(self, client):
        self.client = client
        self.count, self.requests_count, self.top_urls, self.requests_4xx, self.requests_5xx = parse_log()

    def create_count(self):
        requests_count = RequestsModel(
            count=self.count
        )
        self.client.session.add(requests_count)
        self.client.session.commit()

    def create_requests_type(self):
        items = list(self.requests_count.items())
        data = [RequestsTypeModel(type=i[0], count=i[1]) for i in items]
        self.client.session.add_all(data)
        self.client.session.commit()
        return len(items)

    def create_top_requests(self, rownum):
        if rownum > len(self.top_urls):
            rownum = len(self.top_urls)
        data = [TopRequestsModel(url=self.top_urls[i][0], count=self.top_urls[i][1]) for i in range(rownum)]
        self.client.session.add_all(data)
        self.client.session.commit()

    def create_client_error(self, rownum):
        if rownum > len(self.requests_4xx):
            rownum = len(self.requests_4xx)
        data = [BiggestClientErrModel(url=self.requests_4xx[i][0],
                                      status_code=self.requests_4xx[i][1],
                                      bytes_sent=self.requests_4xx[i][2],
                                      ip=self.requests_4xx[i][3]) for i in range(rownum)]
        self.client.session.add_all(data)
        self.client.session.commit()

    def create_server_error(self, rownum):
        if rownum > len(self.requests_5xx):
            rownum = len(self.requests_5xx)
        data = [BiggestServerErrModel(ip=self.requests_5xx[i][0],
                                      count=self.requests_5xx[i][1]) for i in range(rownum)]
        self.client.session.add_all(data)
        self.client.session.commit()
