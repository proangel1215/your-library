import requests


class BookGoogleApi:
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def search_books(self, query):
        try:
            params = {"q": query}
            response = requests.get(f"{self.api_base_url}volumes", params=params)
            print(response.status_code)
            if response.status_code == 200:
                return {"status": "ok", "books": response.json()["items"]}
            else:
                response.raise_for_status()

        except requests.RequestException as e:
            # Handle request exceptions (e.g., network issues)
            print(f"Error during search_books request: {e}")
            return {"status": "error", "books": []}
        
        
    def get_book_details(self, book_id):
        try:
           
            response = requests.get(f'{self.api_base_url}volumes/{book_id}')

            if response.status_code == 200:
                
                return self.return_book_dict_from_api_result(response.json())
            else:
                response.raise_for_status()

        except requests.RequestException as e:
            print(f'Error during get_book_details request: {e}')
            return None
        
    def return_book_dict_from_api_result(self, book_data_api):
        book = {
                "id": book_data_api["id"],
            }

        book_data_api = book_data_api["volumeInfo"]

        book["title"]= book_data_api["title"],
        

        if "authors" in book_data_api:
            book["authors"] = book_data_api["authors"]
        else:
            book["authors"] = []

        if "description" in book_data_api:
            book["description"] = book_data_api["description"]
        else:
            book["description"] = ""

        if "publishedDate" in book_data_api:
            book["publishedDate"] = book_data_api["publishedDate"]
        else:
            book["publishedDate"] = []

        if "imageLinks" in book_data_api:
            book["image_url"] = book_data_api["imageLinks"]["thumbnail"]
        else:
            book["publishedDate"] = None
            
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


