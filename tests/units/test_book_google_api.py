from unittest.mock import MagicMock, patch
from app.BookGoogleApi import BookGoogleApi


def test_search_books():
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200

        books_data = [
            {
                "id": "idbook1",
                "volumeInfo": {
                    "title": "Title 1",
                    "subtitle": "Apprenez simplement les bases de la programmation",
                    "authors": ["author 1"],
                    "publishedDate": "2009-12-04",
                    "description": "desc 1",
                },
            },
            {
                "id": "idbook2",
                "volumeInfo": {
                    "title": "Title 2",
                    "subtitle": "Apprenez simplement les bases de la programmation",
                    "authors": ["author 2", "author 3"],
                    "publishedDate": "2009-12-04",
                    "description": "desc 3",
                },
            },
        ]

        books = {"kind": "books#volumes", "items": books_data}

        mock_response.json.return_value = books

        mock_get.return_value = mock_response

        api = BookGoogleApi(api_base_url="https://example.com/api")

        result = api.search_books("Flask Web Development")

        assert result == {"status": "ok", "books": books_data}


def test_search_details_book():
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200

        book_data = {
            "id": "idbook1",
            "volumeInfo": {
                "title": "Title 1",
                "subtitle": "Apprenez simplement les bases de la programmation",
                "authors": ["author 1"],
                "publishedDate": "2009-12-04",
                "description": "desc 1",
            },
        }

        mock_response.json.return_value = book_data

        mock_get.return_value = mock_response

        api = BookGoogleApi(api_base_url="https://example.com/api")

        result = api.search_book_details("id")

        assert result == {"status": "ok", "book": book_data}



# def test_search_books_error_handling():
#     with patch("requests.get") as mock_get:
#         mock_response = MagicMock()
#         mock_response.status_code = 404

#         mock_get.return_value = mock_response

#         api = BookGoogleApi(api_base_url="https://example.com/api")

#         result = api.search_books("Nonexistent Query")
#         assert result is not None
