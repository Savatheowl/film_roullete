from src.app import app_run
from src.database import init_db
from src.api_fetcher import get_genre_list, SortBy

import asyncio


async def main():
    init_db()
    await get_genre_list()
    app_run()
    

if __name__ == "__main__":
    asyncio.run(main())
