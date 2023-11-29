from flask import Blueprint, render_template, request
from flask_login import login_required
from .forms import SearchBookForm
from .BookGoogleApi import BookGoogleApi
from dotenv import load_dotenv
import os

project_folder = os.path.expanduser("")
load_dotenv(os.path.join(project_folder, ".env"))

books = Blueprint("books", __name__)

DB_PORT = os.getenv("DB_PORT")


@books.route("/", methods=["GET", "POST"])
@login_required
def home():
    form = SearchBookForm()
    books_results = []

    if request.method == "POST" and form.validate_on_submit():
        search_str = form.search.data
        google_api_url = os.getenv("GOOGLE_API_URL")

        book_google_api = BookGoogleApi(google_api_url)

        books_results = book_google_api.get_results_books_api(search_str)

    return render_template("books/home.html", form=form, books_results=books_results)
