from flask import Blueprint, render_template, request
from flask_login import login_required
from .forms import SearchBookForm
import requests
import json 

books = Blueprint("books", __name__)


@books.route("/", methods=["GET", "POST"])
@login_required
def home():
    form = SearchBookForm()

    if request.method == "POST" and form.validate_on_submit():

        search_str = form.search.data

        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={search_str}')

        books_results = []

        if response.status_code == 200:
            results = response.json()['items']
            for result in results:
                print(result['volumeInfo']['authors'])
                # books_results.append({
                #     "id": result['id'],
                #     "title": result['volumeInfo']['title'],
                #     "author": result['volumeInfo']['authors'][0],
                #     # "description": result['description'],
                #     "publishedDate": result['volumeInfo']['publishedDate'],
                # })

            # print(results)


    

    return render_template("books/home.html", form=form, books_results=results)
