from flask import Blueprint, render_template, request
from flask_login import login_required

from app.tools.db import (
    get_question,
)


routes = Blueprint("questions", __name__, url_prefix="/questions")


@routes.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        return render_template("questions.html")
    else:
        questions = get_question(search_string=request.form["search_string"])
        return render_template("questions.html", questions=questions, search_string=request.form["search_string"])
