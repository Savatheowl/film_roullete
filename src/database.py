from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import
from contextlib import contextmanager


global_engine = None
def _get_engine():
    global engine
    if engine is None:
        engine = create_engine("sqlite:///database.db", echo=True)
    return engine

Session = sessionmaker(bind=engine)
@contextmanager
def make_session(engine: Engine):
    try:
        session = Session(bind=_get_engine())
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


class Base(declarative_base()):
    pass



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
