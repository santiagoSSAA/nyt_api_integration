import pytest
from app.services.memory_storage import MemoryStorage


@pytest.fixture
def memory_storage():
    """Fixture to create a new instance of MemoryStorage."""
    return MemoryStorage()


@pytest.mark.asyncio
async def test_add_books(memory_storage):
    """Test adding books to a specific genre."""
    memory_storage.clear_storate()
    genre = "Fiction"
    books = ["Book 1", "Book 2"]

    await memory_storage.add_books(genre, books)

    assert genre in memory_storage.storage
    assert memory_storage.get_books(genre) == books


@pytest.mark.asyncio
async def test_get_books(memory_storage):
    """Test retrieving books from a specific genre."""
    memory_storage.clear_storate()
    genre = "Fiction"
    books = ["Book 1", "Book 2"]

    await memory_storage.add_books(genre, books)

    retrieved_books = memory_storage.get_books(genre)

    assert retrieved_books == books


@pytest.mark.asyncio
async def test_get_all_genres(memory_storage):
    """Test retrieving all genres."""
    memory_storage.clear_storate()
    await memory_storage.add_books("Fiction", ["Book 1"])
    await memory_storage.add_books("Non-Fiction", ["Book 2"])

    genres = memory_storage.get_all_genres()

    assert set(genres) == {"Fiction", "Non-Fiction"}


@pytest.mark.asyncio
async def test_delete_genre(memory_storage):
    """Test deleting a genre."""
    memory_storage.clear_storate()
    genre = "Fiction"
    await memory_storage.add_books(genre, ["Book 1"])
    memory_storage.delete_genre(genre)

    with pytest.raises(KeyError):
        memory_storage.get_books(genre)


def test_delete_non_existing_genre(memory_storage):
    """Test deleting a genre that does not exist."""
    memory_storage.clear_storate()
    genre = "Non-Existing"

    memory_storage.delete_genre(genre)
    assert memory_storage.get_all_genres() == []
