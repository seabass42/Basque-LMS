from flask import render_template, Blueprint, redirect, url_for, flash, request
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

auth = Blueprint('auth', __name__, template_folder='templates')

# http://127.0.0.1:5000


@auth.route('/login', methods=['GET'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main.home"))
        else:
            flash("Invalid username or password")

    return render_template("login.html")


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
