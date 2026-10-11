from contextlib import contextmanager
from datetime import datetime
from hashlib import sha256

from sqlalchemy import (DateTime, Engine, Integer, String, Text, create_engine,
                        text, insert)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
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


class RequestCache(Base):
    __tablename__ = "request_cache"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # при запросе сав сделай чтобы сначала была обработка, что пришел корректный запрос, а потом запись в БД
    request: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    response: Mapped[str] = mapped_column(String, nullable=False)
    response_hash: Mapped[str] = mapped_column(String, nullable=False)
    requested_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now()
    )


class Genres(Base):
    __tablename__ = "genres"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    tmdb_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    name_ru: Mapped[str] = mapped_column(String, nullable=False)
    name_en: Mapped[str] = mapped_column(String, nullable=False)
    

def add_or_update_genre(tmdb_id: int = None, name_ru: str = None, name_en: str = None) -> None:
    stmt = sqlite_insert(Genres).values(tmdb_id=tmdb_id, name_ru=name_ru, name_en=name_en)

    # Если жанр с таким tmdb_id уже есть — обновляем name_ru и name_en
    stmt = stmt.on_conflict_do_update(index_elements=["tmdb_id"], set_=dict(name_ru=name_ru, name_en=name_en))

    with make_session() as s:
        s.execute(stmt)
        s.commit()


def add_or_update_bunch_genres(genres: list[dict]) -> None:
    pass
    # genres_obj

    
# def save_request(request: str, response) -> None:
#     with make_session() as s:
#         RequestHash(
#             request=request,
#             response=response,
#             response_hash=sha256(response).hexdigest(),
#             requested_at=datetime.now(),
#         )

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
