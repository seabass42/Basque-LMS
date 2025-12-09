from flask import Blueprint, render_template, redirect, request, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user
from app.models import User

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect("/")
        else:
            flash("Incorrect email or password")

    return render_template("login.html")

@auth.route("/logout")
def logout():
    logout_user()
    return redirect("/login")
