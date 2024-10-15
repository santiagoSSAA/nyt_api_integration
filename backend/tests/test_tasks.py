import pytest
from app.services.tasks import fetch_nyt_books
from app.services.memory_storage import MemoryStorage
from app.services.nyt_service import NYTService


@pytest.mark.asyncio
async def test_background_task_success(mocker):
    """
    Test the background task that fetches genres and bestsellers.
    """
    # Setup mocks for NYTService methods
    mock_genres = ["fiction", "non-fiction"]
    mock_books = {"fiction": ["Book 1", "Book 2"], "non-fiction": ["Book 3"]}

    mocker.patch.object(NYTService, 'get_books_genres',
                        return_value=mock_genres)
    mocker.patch.object(NYTService, 'get_current_best_sellers',
                        side_effect=lambda genre: mock_books.get(genre, []))

    # Execute the background task
    await fetch_nyt_books()

    # Assertions on success
    memory_storage = MemoryStorage()
    assert memory_storage.get_all_genres() == mock_genres
    assert memory_storage.get_books("fiction") == mock_books["fiction"]
    assert memory_storage.get_books("non-fiction") == mock_books["non-fiction"]


@pytest.mark.asyncio
async def test_background_task_retry_policy(mocker):
    """
    Test the retry policy in the background task when a 429 is encountered.
    """
    # Mocking the NYTService methods
    mocker.patch.object(NYTService, 'get_books_genres',
                        return_value=["fiction"])
    mocker.patch.object(NYTService, 'get_current_best_sellers',
                        side_effect=[Exception("429"), ["Book 1"]])

    # Execute the background task and assert that it retries
    with pytest.raises(Exception, match="429"):
        await fetch_nyt_books()

    # After retries, check that no books are added to memory storage
    memory_storage = MemoryStorage()
    assert memory_storage.get_all_genres() == ["fiction"]
    assert memory_storage.get_books("fiction") == []
