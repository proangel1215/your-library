from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from .forms import SearchBookForm
from .BookGoogleApi import BookGoogleApi
from dotenv import load_dotenv
import os

project_folder = os.path.expanduser("")
load_dotenv(os.path.join(project_folder, ".env"))

books = Blueprint("books", __name__)


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

        if books_results["status"] == "error":
            flash("An error occured", category="error")

        books_results = books_results["books"]

    return render_template("books/home.html", form=form, books_results=books_results)


@books.route("/books/details/<id>", methods=["GET"])
@login_required
def details(id):
    google_api_url = os.getenv("GOOGLE_API_URL")
    book_google_api = BookGoogleApi(google_api_url)

    result = book_google_api.get_result_book_details(id)

    if result["status"] == "error":
        flash("An error occured", category="error")

    return render_template("books/details.html", book=result["book"])
