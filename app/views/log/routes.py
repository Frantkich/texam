from flask import Blueprint, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user


import app.tools.db as db


routes = Blueprint("log", __name__, url_prefix="/")


@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return """
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               """
    email = request.form["email"]
    user = db.get_user(email)
    if user:
        if request.form["password"] == user["password"]:
            user = db.User()
            user.id = email
            login_user(user)
            return redirect(url_for("log.protected"))
    return "Bad login"


@routes.route("/protected")
@login_required
def protected():
    return "Logged in as: " + current_user.id


@routes.route("/logout")
def logout():
    logout_user()
    return "Logged out"
