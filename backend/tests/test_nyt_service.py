import pytest
import asyncio
from unittest.mock import AsyncMock
from app.services.nyt_service import NYTService
from httpx import HTTPStatusError, RequestError


@pytest.fixture
def nyt_service():
    """Fixture to create an instance of NYTService."""
    return NYTService()


@pytest.mark.asyncio
async def test_get_books_genres_success(nyt_service, mocker):
    """Test getting book genres successfully."""
    # Mock the _make_request method to return a successful response
    mock_response = AsyncMock(return_value={
        "results": [{"list_name": "Fiction"}, {"list_name": "Non-Fiction"}]
    })
    mocker.patch.object(nyt_service, '_make_request', mock_response)

    genres = await nyt_service.get_books_genres()

    assert genres == ["Fiction", "Non-Fiction"]


@pytest.mark.asyncio
async def test_get_books_genres_http_error(nyt_service, mocker):
    """Test handling HTTP errors when getting book genres."""

    # Create a mock response object to pass as the response argument
    mock_response = mocker.Mock()
    mock_response.status_code = 404  # Simula un código de estado HTTP
    mock_response.text = "Not Found"  # Mensaje de error simulado

    # Mock the _make_request method to raise an HTTPStatusError
    mocker.patch.object(
        nyt_service,
        '_retry_policy',
        side_effect=RequestError(message="")
    )

    # Asegúrate de que el método get_books_genres() lanza la excepción
    with pytest.raises(RequestError):
        await nyt_service.get_books_genres()


@pytest.mark.asyncio
async def test_get_current_best_sellers_success(nyt_service, mocker):
    """Test getting current best sellers by genre successfully."""
    genre = "fiction"
    # Mock the _make_request method to return a successful response
    mock_response = AsyncMock(return_value={
        "results": {"books": ["Book 1", "Book 2"]}
    })
    mocker.patch.object(nyt_service, '_make_request', mock_response)

    best_sellers = await nyt_service.get_current_best_sellers(genre)

    assert best_sellers == ["Book 1", "Book 2"]


@pytest.mark.asyncio
async def test_get_current_best_sellers_http_error(nyt_service, mocker):
    """Test handling HTTP errors when getting current best sellers."""
    genre = "fiction"
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"

    mocker.patch.object(
        nyt_service,
        '_retry_policy',
        side_effect=RequestError(message="")
    )

    with pytest.raises(RequestError):
        await nyt_service.get_current_best_sellers(genre)


@pytest.mark.asyncio
async def test_retry_policy_success(nyt_service, mocker):
    """Test the retry policy when the request is successful after retries."""
    genre = "fiction"
    mocker.patch.object(nyt_service, '_make_request', side_effect=[
        RequestError("Error"),
        {
            "results": {"books": ["Book 1"]}
        }
    ])

    best_sellers = await nyt_service.get_current_best_sellers(genre)

    assert best_sellers == ["Book 1"]


@pytest.mark.asyncio
async def test_retry_policy_exceeds_attempts(nyt_service, mocker):
    """Test the retry policy exceeding maximum attempts."""
    genre = "fiction"
    # Mock the _make_request method to always raise an error
    mocker.patch.object(nyt_service, '_make_request',
                        side_effect=RequestError("Error"))

    with pytest.raises(RequestError, match="Max retry attempts exceeded."):
        await nyt_service.get_current_best_sellers(genre)
