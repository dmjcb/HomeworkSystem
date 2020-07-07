from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Stu(Base):
    __tablename__ = 'Stu'
    id = Column(String(32), primary_key=True)
    name = Column(String(32))
    classes = Column(String(32))


class Work(Base):
    __tablename__ = 'Work'
    id = Column(String(32), primary_key=True)
    name = Column(String(32), primary_key=True)
    classes = Column(String(32))
    amount = Column(Integer)
    time = Column(DateTime)
    status = Column(String(32))


class Record(Base):
    __tablename__ = 'Record'
    id = Column(String(32), primary_key=True)
    work_id = Column(String(32))
    stu_id = Column(String(32))
    time = Column(DateTime)


sqlite_url = 'sqlite:///Info.db?check_same_thread=False'

# 创建引擎
engine = create_engine(sqlite_url)

# 创建表
Base.metadata.create_all(engine)

# 创建DBSession类型:
Session = sessionmaker(bind=engine)

# 创建Session类实例
session = Session()
