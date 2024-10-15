import pytest
from app.services.tasks import fetch_nyt_books
from app.services.memory_storage import MemoryStorage
from app.services.nyt_service import NYTService


@pytest.mark.asyncio
async def test_background_task_success(mocker):
    """
    Test the background task that fetches genres and bestsellers.
    """
    mock_genres = ["fiction", "non-fiction"]
    mock_books = {"fiction": ["Book 1", "Book 2"], "non-fiction": ["Book 3"]}

    mocker.patch.object(NYTService, 'get_books_genres',
                        return_value=mock_genres)
    mocker.patch.object(NYTService, 'get_current_best_sellers',
                        side_effect=lambda genre: mock_books.get(genre, []))

    # this will take 12 seconds due an asyncio.sleep (API rate limit)
    await fetch_nyt_books()

    memory_storage = MemoryStorage()
    assert memory_storage.get_all_genres() == mock_genres
    assert memory_storage.get_books("fiction") == mock_books["fiction"]
    assert memory_storage.get_books("non-fiction") == mock_books["non-fiction"]


@pytest.mark.asyncio
async def test_background_task_retry_policy(mocker):
    """
    Test the retry policy in the background task when a 429 is encountered.
    """
    memory_storage = MemoryStorage()
    memory_storage.clear_storate()
    mocker.patch.object(NYTService, 'get_books_genres',
                        return_value=["fiction"])
    mocker.patch.object(NYTService, 'get_current_best_sellers',
                        side_effect=[Exception("429"), ["Book 1"]])

    with pytest.raises(Exception, match="429"):
        await fetch_nyt_books()  # 12 seconds delay due API rate limit

    assert not memory_storage.get_all_genres()
