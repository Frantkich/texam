from flask import Blueprint, render_template


routes = Blueprint("admin", __name__, url_prefix="/admin")


@routes.route("/")
def index():
    return render_template("index.html")
