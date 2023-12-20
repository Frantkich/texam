from flask import Blueprint, render_template, request
from flask_login import login_required
import json

from app.tools.db import create_exam, add_exam_questions, get_exam, get_all_exam, update_exam_questions

routes = Blueprint("exam", __name__, url_prefix="/exam")

@routes.route("/")
@login_required
def index():
    return render_template("exams.html", exams=get_all_exam())

@routes.route("/<exam_name>")
@login_required
def exam(exam_name: str):
    return render_template("exam.html", exam=get_exam(exam_name))

@routes.route("/saveAnswers", methods=["POST"])
@login_required
def save_answers():
    examData = json.loads(request.data)
    update_exam_questions(examData["name"], examData["questions"])
    return 