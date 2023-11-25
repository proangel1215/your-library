from flask import Blueprint, render_template
from flask_login import login_required

books = Blueprint("books", __name__)


@books.route("/home", methods=["GET", "POST"])
@login_required
def home():
    return render_template("books/home.html")
