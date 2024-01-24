from flask import Blueprint, render_template, request
from flask_login import login_required

from app.tools.db.methods import search_questions


routes = Blueprint("questions", __name__, url_prefix="/questions")


@routes.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        exam = type('obj', (object,), {'questions' : []})
        return render_template("questions.html", exam=exam)
    else:
        exam = type('obj', (object,), {
            'questions' : search_questions(search_string=request.form["search_string"])
        })
        return render_template("questions.html", exam=exam, search_string=request.form["search_string"])
