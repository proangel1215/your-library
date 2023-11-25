from flask import Blueprint, render_template, request, flash, redirect
from .forms import RegisterForm, LoginForm
from .models.User import User
from . import db
from sqlalchemy.exc import IntegrityError

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


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
                else:
                    user = User(
                        username=pseudo, email=email, password_plaintext=password
                    )
                    db.session.add(user)
                    db.session.commit()
                    # login_user(new_user, remember=True)
                    return redirect("/home")
            except IntegrityError as message:
                db.session.rollback()
                if "UNIQUE constraint failed: users.email" in str(message):
                    flash(f'ERROR! Email ({email}) already exists in the database.')

                elif "UNIQUE constraint failed: users.username" in str(message):
                    flash(f'ERROR! Username ({pseudo}) already exists in the database.')

            except AssertionError as message:
                flash(
                    " : {}".format(message),
                    category="error",
                )

    return render_template("register.html", form=form)
