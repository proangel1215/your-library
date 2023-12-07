from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from .forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError
from .models.User import User
from . import db
from oauthlib.oauth2 import WebApplicationClient
import requests
import os
import json

auth = Blueprint("auth", __name__)


GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@auth.route("/google-login", methods=["GET"])
def google_login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )

    return redirect(request_uri)


@auth.route("/google-login/callback")
def callback():
    # Get authorization code Google
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get token
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the token
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        user_email = userinfo_response.json()["email"]
        user_name = userinfo_response.json()["given_name"]

        user = User.query.filter_by(google_id=unique_id).first()
        if not user:
            user = User(email=user_email, username=user_name, google_id=unique_id)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect(url_for("books.home"))

    else:
        flash("User email not available or not verified by Google.", category="error")
        return redirect(url_for("auth.login"))


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
            login_user(user)
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
                    # login_user(user, remember=True)
                    return redirect(url_for("books.home"))
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
