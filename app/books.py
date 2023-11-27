from flask import Blueprint, render_template
from flask_login import login_required
from .forms import SearchBookForm

books = Blueprint("books", __name__)


@books.route("/", methods=["GET", "POST"])
@login_required
def home():
    form = SearchBookForm()

    return render_template("books/home.html", form=form)
