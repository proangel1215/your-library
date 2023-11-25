from flask import Blueprint, render_template, request, flash, redirect
from .forms import RegisterForm
from .models.User import User
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/", methods=["GET", "POST"])
def login():
    return "login"


@auth.route("/home", methods=["GET", "POST"])
def home():
    return "home"


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if request.method == "POST":
        if form.validate_on_submit():
            email = request.form.get("email")
            pseudo = request.form.get("pseudo")
            password = request.form.get("password")
            password_confirmation = request.form.get("password_confirmation")
            

            try:
                if password != password_confirmation:
                    raise AssertionError("Password dont match !")

                existing_user = User.query.filter_by(email=email).first()

                if existing_user:
                    raise AssertionError("email already exists")
                else:
                    user = User(
                        username=pseudo, email=email, password_plaintext=password
                    )
                    db.session.add(user)
                    db.session.commit()
                    # login_user(new_user, remember=True)
                    return redirect("/home")
            except AssertionError as message:
                flash(
                    " : {}".format(message),
                    category="error",
                )

    return render_template("register.html", form=form)
