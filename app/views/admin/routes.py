from flask import Blueprint, render_template


routes = Blueprint("admin", __name__, url_prefix="/admin")


@routes.route("/")
def admin():
    return render_template("admin.html")
