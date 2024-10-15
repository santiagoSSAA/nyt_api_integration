import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app  # Asegúrate de importar tu instancia de FastAPI aquí
from app.services.memory_storage import MemoryStorage


@pytest.fixture
def client():
    """Fixture para crear un cliente de prueba de FastAPI."""
    return TestClient(app)


@pytest.fixture
def mock_memory_storage(mocker):
    """Fixture para simular MemoryStorage."""
    mock_storage = mocker.patch("app.services.memory_storage.MemoryStorage")
    return mock_storage.return_value


def test_get_book_genre_list(client, mock_memory_storage):
    """Test para la ruta /books/genres."""
    # Configura el almacenamiento en memoria para devolver géneros
    mock_memory_storage.get_all_genres.return_value = [
        "Fiction", "Non-Fiction"]

    response = client.get("/books/genres")

    assert response.status_code == 200
    assert response.json() == {"message": "ok", "content": [
        "Fiction", "Non-Fiction"]}
    mock_memory_storage.get_all_genres.assert_called_once()


def test_get_best_sellers_by_genre_success(client, mock_memory_storage):
    """Test para la ruta /books/{genre}/best-sellers con un género válido."""
    genre = "Fiction"
    mock_memory_storage.get_books.return_value = [
        {"title": "Best Seller 1", "author": "Author 1"},
        {"title": "Best Seller 2", "author": "Author 2"},
    ]

    response = client.get(f"/books/{genre}/best-sellers")

    assert response.status_code == 200
    assert response.json() == {"books": [
        {"title": "Best Seller 1", "author": "Author 1"},
        {"title": "Best Seller 2", "author": "Author 2"},
    ]}
    mock_memory_storage.get_books.assert_called_once_with(genre="Fiction")


def test_get_best_sellers_by_genre_no_genre(client):
    """Test para la ruta /books/{genre}/best-sellers sin un género."""
    response = client.get("/books//best-sellers")

    # FastAPI devuelve un error 422 si el parámetro no es válido
    assert response.status_code == 422


def test_get_best_sellers_by_genre_empty(client, mock_memory_storage):
    """Test para la ruta /books/{genre}/best-sellers con un género que no tiene libros."""
    genre = "Non-Fiction"
    mock_memory_storage.get_books.return_value = []

    response = client.get(f"/books/{genre}/best-sellers")

    assert response.status_code == 200
    assert response.json() == {"books": []}
    mock_memory_storage.get_books.assert_called_once_with(genre="Non-Fiction")
