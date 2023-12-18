from flask import Blueprint, render_template
from flask_login import login_required
from app.tools.db import create_exam, add_exam_questions, get_exam, get_all_exam

routes = Blueprint("exam", __name__, url_prefix="/exam")

@routes.route("/")
@login_required
def index():
    return render_template("exams.html", exams=get_all_exam())
