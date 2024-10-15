from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.services.memory_storage import MemoryStorage

router = APIRouter()
memory_storage = MemoryStorage()


@router.get("/books/genres")
async def get_book_genre_list():
    return JSONResponse(content={"message": "ok", "content": memory_storage.get_all_genres()})


@router.get("/books/{genre}/best-sellers")
async def get_best_sellers_by_genre(genre: str):
    if not genre:
        return HTTPException(status_code=400, detail="No genre provided")
    genre = genre.replace("_", " ")
    books = memory_storage.get_books(genre=genre)
    return JSONResponse(content={"books": books if books else []})
