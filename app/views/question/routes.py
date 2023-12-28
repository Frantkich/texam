from flask import Blueprint, render_template, request, abort
from flask_login import login_required
import json

from app.tools.helpers import (
    return_error,
    return_success,
    return_data
)
from app.tools.db import (
    get_question,
    get_all_questions
)
from .func import fetch_new_questions, fetch_new_questions


routes = Blueprint("questions", __name__, url_prefix="/questions")


@routes.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        return render_template("questions.html")
    else:
        questions =get_question(search_string=request.form["search_string"])
        print(questions)
        return render_template("questions.html", questions=questions, search_string=request.form["search_string"])
