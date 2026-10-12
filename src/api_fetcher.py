# модуль занимается подтягиванием данных из API и сохраняет их в БД через database.py
import httpx
import asyncio
from enum import Enum

from src.config import Config
from typing import Any
import src.database as db
from datetime import timedelta, datetime

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


class SortBy(Enum):
    original_title_asc = "original_title.asc"
    original_title_desc = "original_title.desc"
    popularity_asc = "popularity.asc"
    popularity_desc = "popularity.desc"
    revenue_asc = "revenue.asc"
    revenue_desc = "revenue.desc"
    primary_release_date_asc = "primary_release_date.asc"
    primary_release_date_desc ="primary_release_date.desc"
    title_asc = "title.asc"
    title_desc = "title.desc"
    vote_average_asc = "vote_average.asc"
    vote_average_desc = "vote_average.desc"
    vote_count_asc = "vote_count.asc"
    vote_count_desc = "vote_count.desc"


# сделать выбор для пользователя ru или eng написание? перевод всего сйта изза этого?
async def get_film_list(include_adult: bool, language: str, page: int, sort_by: SortBy = SortBy.popularity_asc) -> dict:
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult={include_adult}&include_video=false&language={language}&page={page}&sort_by={sort_by}"
    
    cache_id: int | None = db.find_in_cache_by_request(url)
    if cache_id:
        print("Найден кэш")
        cached_request = db.get_cache_by_id(cache_id)
        if (datetime.fromisoformat(cached_request.requested_at) - datetime.now()) <= timedelta(days=7):
            print("Кэш берем, он свежий")
            return cached_request.response
    print("делаем запрос")
    response = await _get_sth_base(url)
    print("кэшируем запрос")
    db.cache_request(
        request=url,
        response=response
    )
    return response
    
    

async def film_serch_query(query: str) -> dict:
    pass

async def main():
    result = await get_genre_list()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())