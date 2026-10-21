# модуль занимается подтягиванием данных из API и сохраняет их в БД через database.py
import asyncio
import json
from datetime import datetime, timedelta
from enum import Enum
from typing import Any
from urllib.parse import quote

import httpx

import src.database as db
from src.config import Config

# api have limitation around 40 requests per second
REQUEST_PS = 35

config = Config()

HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {Config.TMDB_BEARER_TOKEN}",
}


class SortBy(Enum):
    original_title_asc = "original_title.asc"
    original_title_desc = "original_title.desc"
    popularity_asc = "popularity.asc"
    popularity_desc = "popularity.desc"
    revenue_asc = "revenue.asc"
    revenue_desc = "revenue.desc"
    primary_release_date_asc = "primary_release_date.asc"
    primary_release_date_desc = "primary_release_date.desc"
    title_asc = "title.asc"
    title_desc = "title.desc"
    vote_average_asc = "vote_average.asc"
    vote_average_desc = "vote_average.desc"
    vote_count_asc = "vote_count.asc"
    vote_count_desc = "vote_count.desc"


async def _get_sth_base(url: str) -> Any:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        return json.loads(response.text)


def save_genres_to_db(response: dict) -> None:
    genres = response.get("genres", [])
    for genre in genres:
        db.add_or_update_genre(
            tmdb_id=genre["id"],
            name_en=genre["name"],
            name_ru=genre["name_ru"],
        )


async def _in_cache_check(request: str, cache_ttl: timedelta = timedelta(days=7)) -> dict:
    cache_id: int | None = db.find_in_cache_by_request(request)
    if cache_id:
        cached_request = db.get_cache_by_id(cache_id)
        if (cached_request.requested_at - datetime.now()) <= cache_ttl:
            return json.loads(cached_request.response)
    response = await _get_sth_base(request)
    db.cache_request(request=request, response=response)
    return response


# Надо подумать чтобы перевести с БД. То есть чтобы не сохранялось в БД, а извлекалось из кэшированных API запросов, как везде крч
async def get_genre_list() -> None:
    response_en = await _in_cache_check(
        "https://api.themoviedb.org/3/genre/movie/list?language=en"
    )
    response_ru = await _in_cache_check(
        "https://api.themoviedb.org/3/genre/movie/list?language=ru"
    )

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

    for genre_ru, genre_en in zip(response_ru["genres"], response_en["genres"]):
        genre_en["name_ru"] = genre_ru["name"].title()

    save_genres_to_db(response_en)


# сделать выбор для пользователя ru или eng написание? перевод всего сйта изза этого?
async def get_film_list(
    include_adult: bool,
    language: str,
    page: int,
    sort_by: SortBy = SortBy.popularity_asc,
) -> dict:
    url: str = f"https://api.themoviedb.org/3/discover/movie?include_adult={include_adult}&include_video=false&language={language}&page={page}&sort_by={sort_by}"
    response: dict = await _in_cache_check(url)
    return response


async def film_serch_query(
    query: str, include_adult: bool = False, language: str = "en-US", page: int = 1
) -> dict:
    query = quote(query)
    url: str = f"https://api.themoviedb.org/3/search/movie?query={query}&include_adult={include_adult}&language={language}&page={page}"
    response: dict = await _in_cache_check(url)
    return response


# код русского "ru" работает, страницу можно не менять потому что 20 похожих достаточно
async def get_similar_films(
    tmdb_id: int, language: str = "en-US", page: int = 1
) -> dict:
    url: str = f"https://api.themoviedb.org/3/movie/{tmdb_id}/similar?language={language}&page={page}"
    response: dict = await _in_cache_check(url)
    return response


async def main():
    result = await get_genre_list()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
