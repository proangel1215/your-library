from flask import Blueprint

auth = Blueprint("auth", __name__)


@auth.route("/", methods=["GET", "POST"])
def login():
    return "login"
