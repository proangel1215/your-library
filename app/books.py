from flask import Blueprint, render_template, request
from flask_login import login_required
from .forms import SearchBookForm

from .BookGoogleApi import BookGoogleApi

books = Blueprint("books", __name__)


@books.route("/", methods=["GET", "POST"])
@login_required
def home():
    form = SearchBookForm()

    books_results = []

    if request.method == "POST" and form.validate_on_submit():
        search_str = form.search.data
        book_google_api = BookGoogleApi("https://www.googleapis.com/books/v1/volumes")

        results = book_google_api.search_books(search_str)

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

            print(book["authors"])

            if "publishedDate" in result:
                book["publishedDate"] = result["publishedDate"]
            else:
                book["publishedDate"] = []

            if "imageLinks" in result:
                book["image_url"] = result["imageLinks"]["thumbnail"]
            else:
                book["publishedDate"] = None

            books_results.append(book)

    return render_template("books/home.html", form=form, books_results=books_results)
