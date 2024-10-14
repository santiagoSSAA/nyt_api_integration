
import asyncio
from fastapi import FastAPI
import uvicorn

from app.api.routes import router as api_router
from app.services.tasks import (
    scheduler,
    fetch_nyt_books
)
from app.utils.logging import logger


app = FastAPI(title="Book Integration API")
app.include_router(api_router, prefix="/api")


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Book Integration API"}


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(fetch_nyt_books())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
