import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.memory_storage import MemoryStorage


@pytest.fixture
def client():
    """Fixture para crear un cliente de prueba de FastAPI."""
    return TestClient(app)


def test_get_book_genre_list(client, mocker):
    mocker.patch.object(MemoryStorage, "get_all_genres",
                        return_value=["Fiction", "Non-Fiction"])

    response = client.get("api/books/genres")

    assert response.status_code == 200
    assert response.json() == {"message": "ok", "content": [
        "Fiction", "Non-Fiction"]}


def test_get_best_sellers_by_genre_success(client, mocker):
    genre = "Fiction"
    mocker.patch.object(MemoryStorage, "get_all_genres",
                        return_value=["Fiction"])
    mocker.patch.object(MemoryStorage, "get_books",
                        return_value=[
                            {"title": "Best Seller 1", "author": "Author 1"},
                            {"title": "Best Seller 2", "author": "Author 2"},
                        ])

    response = client.get(f"api/books/{genre}/best-sellers")

    assert response.status_code == 200
    assert response.json() == {"books": [
        {"title": "Best Seller 1", "author": "Author 1"},
        {"title": "Best Seller 2", "author": "Author 2"},
    ]}


def test_get_best_sellers_by_genre_no_genre(client):
    response = client.get("api/books//best-sellers")
    assert response.status_code == 404
