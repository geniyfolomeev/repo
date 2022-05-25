import pytest
from client import MysqlClient
from builder import MysqlBuilder
from models import RequestsModel, RequestsTypeModel, TopRequestsModel, BiggestClientErrModel, BiggestServerErrModel


class MyTest:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql: MysqlClient = mysql_client
        self.builder: MysqlBuilder = MysqlBuilder(self.mysql)
        self.table_model = RequestsModel

        self.prepare()

    def get_table(self, **filters):
        self.mysql.session.commit()
        res = self.mysql.session.query(self.table_model).filter_by(**filters)
        return res.all()


class TestCount(MyTest):
    rownum = 1

    def prepare(self):
        self.table_model = RequestsModel
        self.mysql.create_table(self.table_model.__tablename__)
        self.builder.create_count()

    def test_requests_count(self):
        count = self.get_table()
        assert len(count) == self.rownum


class TestRequestsType(MyTest):
    rownum = None

    def prepare(self):
        self.table_model = RequestsTypeModel
        self.mysql.create_table(self.table_model.__tablename__)
        self.rownum = self.builder.create_requests_type()

    def test_requests_type(self):
        count = self.get_table()
        assert len(count) == self.rownum


class TestTopRequests(MyTest):
    rownum = 10

    def prepare(self):
        self.table_model = TopRequestsModel
        self.mysql.create_table(self.table_model.__tablename__)
        self.builder.create_top_requests(rownum=self.rownum)

    def test_requests_type(self):
        count = self.get_table()
        assert len(count) == self.rownum


class TestClientError(MyTest):
    rownum = 5

    def prepare(self):
        self.table_model = BiggestClientErrModel
        self.mysql.create_table(self.table_model.__tablename__)
        self.builder.create_client_error(rownum=self.rownum)

    def test_requests_type(self):
        count = self.get_table()
        assert len(count) == self.rownum


class TestServerError(MyTest):
    rownum = 5

    def prepare(self):
        self.table_model = BiggestServerErrModel
        self.mysql.create_table(self.table_model.__tablename__)
        self.builder.create_server_error(rownum=self.rownum)

    def test_requests_type(self):
        count = self.get_table()
        assert len(count) == self.rownum
