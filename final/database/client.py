import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
import database.models as models
from sqlalchemy.sql.schema import Table


class MysqlClient:

    def __init__(self, db_name, user, password):
        self.user = 'root'
        self.port = 3306
        self.password = 'pass'
        self.host = '127.0.0.1'
        self.db_name = db_name

        self.connection = None
        self.engine = None
        self.session = None
        self.table: Table = models.Base.metadata.tables["test_users"]

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url, max_overflow=5)
        self.connection = self.engine.connect()
        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def insert_data(self, user_data: dict):
        self.connect()
        user = self.table.insert().values(user_data)
        self.connection.execute(user)
        self.connection.close()

    def delete_by_username(self, username: str):
        self.connect()
        data_to_delete = self.table.delete().where(self.table.c.username == username)
        self.connection.execute(data_to_delete)
        self.connection.close()

    def get_row_by_username(self, username) -> list:
        self.connect()
        self.session.commit()
        query = select(self.table).filter(self.table.c.username == username)
        fields = self.session.execute(query)
        self.connection.close()
        return [i._asdict() for i in fields]

    def update_user_data(self, user_data: dict, username):
        self.connect()
        user = self.table.update().values(user_data).where(self.table.c.username == username)
        self.connection.execute(user)
        self.connection.close()
