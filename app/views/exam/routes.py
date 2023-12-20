from flask import Blueprint, render_template, request, abort
from flask_login import login_required
import json

from app.tools.helpers import (
    return_error,
    return_suceess,
    return_data
)
from app.tools.db import (
    get_exam,
    get_all_exam,
    update_exam_questions,
    create_exam,
    add_exam_question,
)
from .scraper import fetch_new_exams, fetch_new_questions


routes = Blueprint("exam", __name__, url_prefix="/exam")


@routes.route("/")
@login_required
def index():
    return render_template("exams.html", exams=get_all_exam())


@routes.route("/<exam_code>")
@login_required
def exam(exam_code: str):
    exam = get_exam(exam_code)
    if not exam:
        return abort(404)
    return render_template("exam.html", exam=exam)


@routes.route("/answers", methods=["POST"])
@login_required
def save_answers():
    examData = json.loads(request.data)
    if update_exam_questions(examData["code"], examData["questions"]):
        return return_suceess("Answers saved.")
    return return_error(500, "Error saving answers.")


@routes.route("/fetchNewExam", methods=["UPDATE"])
@login_required
def fetchNewExam():
    exams = fetch_new_exams()
    if not exams:
        return return_error(500, "Error fetching exams.")
    for exam in exams:
        if not get_exam(exam["code"]):
            create_exam(exam["name"], exam["code"], exam["description"], exam["class_name"], {"questions": []})
    return return_data(exams)


@routes.route("/fetchNewQuestions/<exam_code>", methods=["UPDATE"])
@login_required
def fetchQuestions(exam_code):
    if add_exam_question(exam_code, fetch_new_questions(exam_code)):
        return return_suceess("New question fetched saved.")
    return return_error(500, "Error saving answers.")
