from flask import Blueprint, request, redirect, url_for, render_template, current_app
from flask_login import login_user, logout_user


from app.tools.db.methods import get_user


routes = Blueprint("user", __name__, url_prefix="")


@routes.route("/login", methods=["GET", "POST"])
def login():
    code = None
    if request.method == "GET": return render_template("login.html", code=code)
    if request.form["secret"] == "wubbalubbadubdub": return render_template("wubbalubbadubdub.html")
    user = get_user(request.form["email"])
    if user and request.form["password"] == user.password:
        if request.form["secret"] != current_app.config["SECRET"] : return render_template("theonlyhtmlfile.html")
        login_user(user)
        return redirect(url_for("main.frontend.index"))
    else:
        code = {
            "error": "error",
            "message": "Invalid email or password"
        }
        return render_template("login.html", code=code)


@routes.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.user.login"))
