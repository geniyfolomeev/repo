from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class RequestsModel(Base):

    __tablename__ = 'requests_count'
    __table_args__ = {'mysql_charset': 'utf8'}

    count = Column(Integer, primary_key=True)


class RequestsTypeModel(Base):

    __tablename__ = 'requests_type'
    __table_args__ = {'mysql_charset': 'utf8'}

    type = Column(String(40), primary_key=True)
    count = Column(Integer)


class TopRequestsModel(Base):

    __tablename__ = 'top_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    num = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(50))
    count = Column(Integer)


class BiggestClientErrModel(Base):

    __tablename__ = 'client_error_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    num = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(50))
    status_code = Column(Integer)
    bytes_sent = Column(Integer)
    ip = Column(String(15))


class BiggestServerErrModel(Base):

    __tablename__ = 'server_error_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    num = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15))
    count = Column(Integer)
