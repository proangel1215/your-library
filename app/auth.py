from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from .forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError
from .models.User import User
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Already logged in!  Redirecting to home page...")

        return redirect(url_for("books.home"))

    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.is_password_correct(password):
            flash("Welcome {} !".format(user.username))
            login_user(user, remember=True)
            return redirect(url_for("books.home"))

        flash("Wrong credentials", category="error")

    return render_template("auth/login.html", form=form)


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
                    flash(f"ERROR! Email ({email}) already exists in the database.")

                elif "UNIQUE constraint failed: users.username" in str(message):
                    flash(f"ERROR! Username ({pseudo}) already exists in the database.")

            except AssertionError as message:
                flash(
                    " : {}".format(message),
                    category="error",
                )

    return render_template("auth/register.html", form=form)


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
