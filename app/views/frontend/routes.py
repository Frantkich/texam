from flask import Blueprint, render_template


routes = Blueprint("frontend", __name__, url_prefix="/")


@routes.route("/")
def index():
    return render_template("index.html")
