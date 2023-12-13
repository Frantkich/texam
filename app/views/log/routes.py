from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_user, logout_user


import app.tools.db as db


routes = Blueprint("log", __name__)


@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET": return render_template("login.html")
    print(request.form)
    email = request.form["email"]
    user = db.get_user(email)
    print(user)
    if user:
        if request.form["password"] == user["password"]:
            user = db.User()
            user.id = email
            login_user(user)
            return redirect(url_for("frontend.index"))
    return redirect(url_for("log.login"))


@routes.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("log.login"))
