import requests


class BookGoogleApi:
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def search_books(self, query):
        try:
            params = {"q": query}
            response = requests.get(f"{self.api_base_url}volumes", params=params)

            if response.status_code == 200:
                return response.json()["items"]
            else:
                response.raise_for_status()  # Raises an HTTPError for bad responses

        except requests.RequestException as e:
            # Handle request exceptions (e.g., network issues)
            print(f"Error during search_books request: {e}")
            return None

    def get_results_books_api(self, search_str):
        results = self.search_books(search_str)

        books = []

        for result in results:
            book = {
                "id": result["id"],
            }

            result = result["volumeInfo"]

            book = {
                "title": result["title"],
            }

            if "authors" in result:
                book["authors"] = result["authors"]
            else:
                book["authors"] = []

            if "description" in result:
                book["description"] = result["description"]
            else:
                book["description"] = ""

            if "publishedDate" in result:
                book["publishedDate"] = result["publishedDate"]
            else:
                book["publishedDate"] = []

            if "imageLinks" in result:
                book["image_url"] = result["imageLinks"]["thumbnail"]
            else:
                book["publishedDate"] = None

            books.append(book)

        return books

    # def get_book_details(self, book_id):
    #     try:
    #         params = {'id': book_id}
    #         response = requests.get(f'{self.api_base_url}/book/{book_id}', params=params)

    #         if response.status_code == 200:
    #             return response.json()['book']
    #         else:
    #             response.raise_for_status()

    #     except requests.RequestException as e:
    #         print(f'Error during get_book_details request: {e}')
    #         return None
