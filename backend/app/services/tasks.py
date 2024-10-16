"""Background Tasks module"""

import asyncio

from app.utils.logging import logger
from app.services.nyt_service import NYTService
from app.services.memory_storage import MemoryStorage

memory_storage = MemoryStorage()
nyt_service = NYTService()


async def fetch_nyt_books():
    genres: list = await nyt_service.get_books_genres()
    if not genres:
        logger.warning("No genres on memory storage.")
        return
    logger.info("Updating NYT Best sellers's catalog in the background.")
    for genre in genres:
        await asyncio.sleep(12)
        best_sellers = await nyt_service.get_current_best_sellers(genre)
        if not best_sellers:
            logger.warning("No best sellers returned for genre %s", genre)
            continue
        await memory_storage.add_books(genre=genre, books=best_sellers)
