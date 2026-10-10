# модуль занимается подтягиванием данных из API и сохраняет их в БД через database.py
import httpx
import asyncio

from src.config import Config
from typing import Any

import json


config = Config()

HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {Config.TMDB_BEARER_TOKEN}"
}



def save_to_db() -> None:
    pass


async def _get_sth_base(url: str) -> Any:
    async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=HEADERS)
            return json.loads(response.text)

async def get_genre_list(language: str) -> Any:
    url = f"https://api.themoviedb.org/3/genre/movie/list?language={language}"
    response = await _get_sth_base(url)
    return response



async def main():
    print(get_genre_list("en"))

if __name__ == "__main__":
    asyncio.run(main())