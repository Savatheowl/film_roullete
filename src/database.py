from sqlalchemy import create_engine, Engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from contextlib import contextmanager
from src.config import Config


global_engine = None
def _get_engine():
    global global_engine
    if global_engine is None:
        global_engine = create_engine(Config.DATABASE_URL, echo=True)
    return global_engine


Session = sessionmaker()
@contextmanager
def make_session(engine: Engine):
    session = None
    try:
        session = Session(bind=engine)
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


class Base(declarative_base()):
    __abstract__ = True


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
