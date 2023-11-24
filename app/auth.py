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
        # if form.validate_on_submit():
            email = request.form.get("email")
            pseudo = request.form.get("pseudo")
            password = request.form.get("password")
            password_confirmation = request.form.get("password_confirmation")

            if password != password_confirmation:
                flash("Les 2 mots de passe ne correspondent pas !", category="error")
                return render_template("register.html", form=form)
            
            
            try:
                user = User(username=pseudo, email=email, password_plaintext=password)
                db.session.add(user)
                db.session.commit()
                # login_user(new_user, remember=True)
                flash("OK !")
                return redirect('/home')
                return render_template("register.html", form=form)
                # return redirect("/home")
            except AssertionError as message:
                flash("Erreur : {}".format(message), category="error") 


    return render_template("register.html", form=form)

