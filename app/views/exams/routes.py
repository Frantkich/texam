from flask import Blueprint, render_template, request, abort, redirect
from flask_login import login_required, current_user
import json

from app.tools.helpers import (
    return_error,
    return_success,
    return_data
)
from app.tools.db import (
    get_exams,
    get_exams,
    update_exam_questions,
    create_exam,
)
import app.views.exams.scraper as scraper

routes = Blueprint("exams", __name__, url_prefix="/exams")


@routes.route("/")
@login_required
def index():
    return render_template("exams.html", exams=get_exams())


@routes.route("/fetch", methods=["UPDATE"])
@login_required
def fetch_new_exam():
    exams = scraper.fetch_new_exams()
    if not exams:
        return return_error(500, "Error fetching exams.")
    for exam in exams:
        if not get_exams(exam["code"]):
            create_exam(exam["name"], exam["code"], exam["description"], exam["class_name"])
    return return_data(exams)


@routes.route("/<exam_code>")
@login_required
def exam(exam_code: str):
    exam = get_exams(exam_code)
    if not exam:
        return abort(404)
    return render_template("exam.html", exam=exam)


@routes.route("/answers/save", methods=["UPDATE"])
@login_required
def answers_save():
    examData = json.loads(request.data)
    if update_exam_questions(examData["code"], examData["questions"]):
        return return_success("Answers saved.")
    return return_error(500, "Error saving answers.")


@routes.route("/start/<exam_code>", methods=["POST"])
@login_required
def start_exam(exam_code):
    if not current_user.exam:
        if scraper.load_questions(exam_code):
            return return_success("Exam started")
        return return_error(500, "Error passing exam.")
    return return_error(500, "Exam already started.")


@routes.route("/active", methods=["GET"])
@login_required
def active_exam():
    if not current_user.exam: return abort(404)
    exam = type('obj', (object,), {
        'name' : current_user.exam.name,
        'code' : current_user.exam.code,
        'questions' : [question for question in current_user.exam.questions if current_user in question.active_for]
    })
    return render_template("activeExam.html", exam=exam)


@routes.route("/answers/submit", methods=["POST"])
@login_required
def answers_submit():
    if not current_user.exam: return return_error(404, "No exam started.")
    report = scraper.answering_questions()
    if not report: return return_error(500, "Error answering exam's questions.")
    return return_success(report)


@routes.route("/submit", methods=["POST"])
@login_required
def submit_exam():
    if not current_user.exam: return return_error(404, "No exam started.")
    result = scraper.submit_exam()
    if not result: return return_error(500, "Error submitting exam.")
    return return_data({"result_id": result.id})
