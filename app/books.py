from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from .forms import SearchBookForm
from .BookGoogleApi import BookGoogleApi
from dotenv import load_dotenv
import os
from .models.Book import Book, Author, Category
from . import db

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


@books.route("/books/add/<id>", methods=["GET"])
@login_required
def add_favorite(id):
    google_api_url = os.getenv("GOOGLE_API_URL")
    book_google_api = BookGoogleApi(google_api_url)

    result = book_google_api.get_result_book_details(id)

    if result["status"] == "ok":
        book_data = result["book"]
        authors = []
        
        # check if the book is already in the db
        book = Book.query.filter_by(google_api_id=id).first()
        
        if book:
            # add the book to the user
            # redirect
            pass 
        else:
            new_book = Book(
                title=book_data["title"],
                google_api_id=book_data["id"],
                image_url=book_data["image_url"],
                description=book_data["description"],
                published_date=book_data["published_date"],
            )
            
            db.session.add(new_book)
            db.session.commit()
            # must check authors, categories and add them if needed
            for author_name in book_data['authors']:
                
                author = Author.query.filter_by(name=author_name).first()
                print(author_name)
                print(author)
                
                if not author:
                    print('ok')
                    author = Author(name=author_name)
                    db.session.add(author)
                    new_book.authors.append(author)
                    db.session.commit()
                authors.append(author)
                                
            # categories = []
            
            for category_name in book_data['categories']:
                
                category = Category.query.filter_by(name=category_name).first()
                
                if not category:
                    category = Category(name=category_name)
                    db.session.add(category)
                    new_book.categories.append(category)
                    db.session.commit()
                
            
        #check if the book is already in db   
            
        
      

    if result["status"] == "error":
        flash("An error occured", category="error")

    return "ok"
    return render_template("books/details.html", book=result["book"])
