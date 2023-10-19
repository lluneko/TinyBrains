from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import exists


db_path = 'db/users_base.sqlite'
Base = declarative_base()
__factory = None


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    Base.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


def add_user(nameus, passwordus, session):
    c = User(name=nameus, password=passwordus)
    session.add(c)
    session.commit()
    return nameus, passwordus


def check_user(login, password, session):
    if session.query(exists().where(User.name == login, User.password == password)).scalar():
        return 'Такой пользователь уже существет'
    return ''
