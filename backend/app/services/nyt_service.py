import os
import asyncio

import httpx
from app.utils.logging import logger
from dotenv import load_dotenv
from httpx import HTTPStatusError, RequestError

load_dotenv()


class NYTService:
    """NYT API Service Class"""
    _instance = None
    RETRY_ATTEMPTS: int = 3
    RETRY_DELAY: int = 2
    API_KEY: str = os.getenv("NYT_API_KEY")
    API_SECRET: str = os.getenv("NYT_API_SECRET")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NYTService, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, 'initialized'):
            self.headers = {
                "Content-Type": "application/json"
            }
            self.params = {"api-key": self.API_KEY}
            self.client = httpx.AsyncClient()
            self.initialized = True

    async def get_books_genres(self) -> list:
        """Get books genres method"""
        url: str = "https://api.nytimes.com/svc/books/v3/lists/names.json"
        logger.info("Attempting request to NYT list names endpoint.")
        api_response = await self._retry_policy(
            func=self._make_request,
            url=url
        )
        return [genre["list_name"] for genre in api_response.get("results", [])]

    async def get_current_best_sellers(self, genre: str) -> list:
        """Get current best sellers by genre method"""
        url: str = f"https://api.nytimes.com/svc/books/v3/lists/current/{genre}.json"
        logger.info(
            "Attempting request to NYT best sellers endpoint for genre %s", genre)
        response = await self._retry_policy(
            func=self._make_request,
            url=url
        )
        return response.get("results", {}).get("books", [])

    async def _make_request(self, url: str, params: dict = None):
        """Make request method for handle retries and logging"""
        request_params = {**self.params}
        if params:
            request_params.update(params)
        try:
            response = await self.client.get(
                url=url, headers=self.headers, params=request_params)
            response.raise_for_status()
            return response.json()
        except HTTPStatusError as http_err:
            logger.error("HTTP error occurred: %s for URL: %s", http_err, url)
            raise
        except RequestError as req_err:
            logger.error(
                "Request error occurred: %s for URL: %s", req_err, url)
            raise

    async def _retry_policy(self, func, *args, **kwargs):
        """Retry policy method for apply retry logic on a request call"""
        attempt = 0
        while attempt < self.RETRY_ATTEMPTS:
            try:
                return await func(*args, **kwargs)
            except (HTTPStatusError, RequestError):
                logger.warning("Attempt %d failed. Retrying...", attempt + 1)
                attempt += 1
                await asyncio.sleep(self.RETRY_DELAY)

        raise RequestError("Max retry attempts exceeded.")
