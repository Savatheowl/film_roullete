from src.app import app_run
from src.database import init_db
from src.api_fetcher import get_genre_list, get_film_list, SortBy

import asyncio


async def main():
    init_db()
    await get_genre_list()
    a = await get_film_list(
        include_adult=True,
        language="ru",
        page=1,
    )
    

if __name__ == "__main__":
    asyncio.run(main())
