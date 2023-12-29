from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user
import json

from app.tools.helpers import (
    return_error,
    return_success,
    return_data
)
from app.tools.db import (
    get_exam,
    get_all_exams,
    update_exam_questions,
    create_exam,
    add_exam_question
)
import app.views.exams.scraper as scraper

routes = Blueprint("exams", __name__, url_prefix="/exams")


@routes.route("/")
@login_required
def index():
    return render_template("exams.html", exams=get_all_exams())


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
        return return_success("Answers saved.")
    return return_error(500, "Error saving answers.")


@routes.route("/fetchNewExam", methods=["UPDATE"])
@login_required
def fetch_new_exam():
    exams = scraper.fetch_new_exams()
    if not exams:
        return return_error(500, "Error fetching exams.")
    for exam in exams:
        if not get_exam(exam["code"]):
            create_exam(exam["name"], exam["code"], exam["description"], exam["class_name"])
    return return_data(exams)


@routes.route("/fetchNewQuestions/<exam_code>", methods=["UPDATE"])
@login_required
def fetchQuestions(exam_code):
    if add_exam_question(exam_code, scraper.fetch_new_questions(exam_code)):
        return return_success("New question fetched saved.")
    return return_error(500, "Error saving answers.")


@routes.route("/startExam/<exam_code>", methods=["POST"])
@login_required
def start_exam(exam_code):
    if not current_user.exam:
        if scraper.pass_exam(exam_code):
            return return_success("Exam started")
        return return_error(500, "Error passing exam.")
    return return_error(500, "Exam already started.")


@routes.route("/active", methods=["GET"])
@login_required
def active_exam():
    if False:
        return render_template("examResults.html", exam=current_user.exam)
    if not current_user.exam:
        return return_error(404, "No exam started.")
    return render_template("activeExam.html", exam=current_user.exam)


@routes.route("/submit", methods=["GET", "POST"])
@login_required
def submit_exam():
    if not current_user.exam:
        return return_error(404, "No exam started.")
    if not scraper.submit_exam():
        return return_error(500, "Error submitting exam.")
    return return_success("Exam submitted.")
