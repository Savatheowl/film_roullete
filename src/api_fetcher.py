# модуль занимается подтягиванием данных из API и сохраняет их в БД через database.py
import httpx
import asyncio

from src.config import Config
from typing import Any
import src.database as db
from src.genre_translations import GENRE_TRANSLATIONS


import json

# api have limitation around 40 requests per second
REQUEST_PS = 35

config = Config()


HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {Config.TMDB_BEARER_TOKEN}"
}



async def _get_sth_base(url: str) -> Any:
    async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=HEADERS)
            return json.loads(response.text)


def save_genres_to_db(response: dict) -> None:
    genres = response.get('genres', [])
    for genre in genres:
        db.add_or_update_genre(
            tmdb_id=genre['id'],
            name_en=genre['name'],
            name_ru=genre['name_ru'],
        )


async def get_genre_list() -> None:
    response_en = await _get_sth_base("https://api.themoviedb.org/3/genre/movie/list?language=en")
    response_ru = await _get_sth_base("https://api.themoviedb.org/3/genre/movie/list?language=ru")

    """
    API result:
        {
          "genres": [
            {
              "id": 28,
              "name": "боевик"
            },
            ...
          ]
        }
    """

    for genre_ru, genre_en in zip(response_ru['genres'], response_en['genres']):
        genre_en['name_ru'] = genre_ru['name'].title()

    save_genres_to_db(response_en)


async def main():
    result = await get_genre_list()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())