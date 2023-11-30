import requests
import re
from datetime import datetime


class BookGoogleApi:
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def search_books(self, query):
        try:
            params = {"q": query}
            response = requests.get(f"{self.api_base_url}volumes", params=params)

            if response.status_code == 200:
                return {"status": "ok", "books": response.json()["items"]}
            else:
                response.raise_for_status()

        except requests.RequestException as e:
            print(f"Error during search_books request: {e}")
            return {"status": "error", "books": []}

    def search_book_details(self, book_id):
        try:
            response = requests.get(f"{self.api_base_url}volumes/{book_id}")

            if response.status_code == 200:
                return {"status": "ok", "book": response.json()}
            else:
                response.raise_for_status()

        except requests.RequestException as e:
            print(f"Error during get_book_details request: {e}")
            return {"status": "error", "book": {}}

    def return_book_dict_from_api_result(self, book_data_api):
        book = {
            "id": book_data_api["id"],
        }

        book_data_api = book_data_api["volumeInfo"]

        book["title"] = (book_data_api["title"],)

        if "authors" in book_data_api:
            book["authors"] = book_data_api["authors"]
        else:
            book["authors"] = []

        if "categories" in book_data_api:
            book["categories"] = book_data_api["categories"]
        else:
            book["categories"] = []

        if "description" in book_data_api:
            book["description"] = book_data_api["description"]
        else:
            book["description"] = ""

        if "publishedDate" in book_data_api:
            book["published_date"] = self.check_and_convert_date(
                book_data_api["publishedDate"]
            )
        else:
            book["published_date"] = None

        if "imageLinks" in book_data_api:
            book["image_url"] = book_data_api["imageLinks"]["thumbnail"]
        else:
            book["image_url"] = None

        return book

    def get_results_books_api(self, search_str):
        results = self.search_books(search_str)

        if results["status"] == "error":
            return results

        books = []

        for result in results["books"]:
            book = self.return_book_dict_from_api_result(result)
            books.append(book)

        return {"status": "ok", "books": books}

    def get_result_book_details(self, id):
        result = self.search_book_details(id)
        print(result)

        if result["status"] == "error":
            return result

        book = self.return_book_dict_from_api_result(result["book"])
        return {"status": "ok", "book": book}

    def check_and_convert_date(self, date):
        # Check if the date matches the year format using a regular expression
        if re.match(r"^\d{4}$", date):
            # If it matches, convert it to the desired format
            formatted_date = f"{date}-01-01"
            return formatted_date
        else:
            # If it doesn't match, return an indication that the format is incorrect
            return None
