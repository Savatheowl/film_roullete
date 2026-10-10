from contextlib import contextmanager
from datetime import datetime
from hashlib import sha256

from sqlalchemy import (DateTime, Engine, Integer, String, Text, create_engine,
                        text)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from src.config import Config

engine = None


def _get_engine():
    global engine
    if engine is None:
        engine = create_engine(Config.DATABASE_URL, echo=True)
    return engine


Session = sessionmaker(bind=_get_engine())


@contextmanager
def make_session():
    try:
        session = Session()
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


class Base(DeclarativeBase):
    __abstract__ = True


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now()
    )


class RequestHash(Base):
    __tablename__ = "request_hash"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # при запросе сав сделай чтобы сначала была обработка что прише лкорректный запрос, а потом запись в БД
    request: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    response: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    response_hash: Mapped[str] = mapped_column(String, nullable=False)
    requested_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now()
    )

def save_request(request: str, response) -> None:
    with make_session() as s:
        RequestHash(
            request=request,
            response=response,
            response_hash=sha256(response).hexdigest(),
            requested_at=datetime.now(),
        )

def db_health_status_message() -> str:
    with make_session() as s:
        row = s.execute(text("SELECT 1")).scalar_one_or_none()
        if row == 1:
            return "All right!"
        return "STH wrong with DB"


def init_db() -> None:
    Base.metadata.create_all(_get_engine())


def main():
    init_db()


if __name__ == "__main__":
    main()
