from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#from .config import db_token

engine = create_engine('postgresql://osubot:qwerty@localhost:5432/botusers')


Session = sessionmaker()

Session.configure(bind=engine, autoflush=False, autocommit=False)

s = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    group_id = Column(CHAR(30), primary_key=False)
    user_id = Column(Integer, primary_key=True)

    @classmethod
    def get_group(cls, id):
        return s.query(User).get(id).group_id

    @classmethod
    def get_user_by_id(cls,id):
        return s.query(User).get(id)

    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id
