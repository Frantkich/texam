from flask import Blueprint, request, redirect, url_for, render_template, current_app
from flask_login import login_user, logout_user


from app.tools.db.methods import get_user


routes = Blueprint("log", __name__)


@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET": return render_template("login.html")
    if request.form["secret"] == "wubbalubbadubdub": return render_template("wubbalubbadubdub.html")
    if request.form["secret"] != current_app.config["SECRET"] : return render_template("theonlyhtmlfile.html")
    user = get_user(request.form["email"])
    if user and request.form["password"] == user.password:
        login_user(user)
        return redirect(url_for("frontend.index"))
    return redirect(url_for("log.login"))


@routes.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("log.login"))
