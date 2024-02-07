from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user
import json

from app.tools.helpers import (
    return_error,
    return_success,
    return_data
)
import app.tools.db.methods as db_methods 
import app.views.exams.scraper as scraper

routes = Blueprint("exams", __name__, url_prefix="/exams")


@routes.route("/")
@login_required
def index():
    return render_template("exams.html")


@routes.route("/fetch/<mode>", methods=["UPDATE"])
@login_required
def fetch_exams(mode:str = "all"):
    if mode == "all":    exams = db_methods.get_exams()
    elif mode == "user": exams = scraper.fetch_user_exams()
    if not exams: return return_error(500, "Error fetching exams.")
    if current_user.role == "0": exams = [exam for exam in exams if exam.for_all]
    exams = [{
        "code": exam.code,
        "name": exam.name
    } for exam in exams]
    return return_data(exams)


@routes.route("/<exam_name>")
@login_required
def exam(exam_name: str):
    """
    View function for displaying an exam.
    """
    exam = db_methods.get_exams(exam_name)
    if not exam:
        return abort(404)
    results = db_methods.get_exam_results(exam.id)
    stats = {
        "passed" : sum([1 for result in results if result.success]),
        "failed" : sum([1 for result in results if not result.success]),
    }
    return render_template("exam.html", exam=exam, stats=stats)


@routes.route("/answers/save", methods=["UPDATE"])
@login_required
def answers_save():
    """
    View function for saving exam answers.
    """
    examData = json.loads(request.data)
    if db_methods.update_exam_questions(examData["name"], examData["questions"]):
        return return_success("Answers saved.")
    return return_error(500, "Error saving answers.")


@routes.route("/start/<exam_name>", methods=["POST"])
@login_required
def start_exam(exam_name):
    """
    View function for starting an exam.
    """
    if not current_user.exam:
        if scraper.load_questions(exam_name):
            return return_success("Exam started")
        return return_error(400, "Error passing exam. (Maybe you already passed it?)")
    return return_error(400, "Exam already started.")


@routes.route("/active", methods=["GET"])
@login_required
def active_exam():
    """
    View function for displaying the active exam.
    """
    if not current_user.exam: return abort(404)
    exam = type('obj', (object,), {
        'name' : current_user.exam.name,
        'code' : current_user.exam.code,
        'questions' : [question for question in current_user.exam.questions if current_user in question.active_for]
    })
    return render_template("activeExam.html", exam=exam)


@routes.route("/active/submit/answers", methods=["POST"])
@login_required
def answers_submit():
    """
    View function for submitting exam answers.
    """
    if not current_user.exam: return return_error(404, "No exam started.")
    report = scraper.answering_questions()
    if not report: return return_error(500, "Error answering exam's questions.")
    return return_success(report)


@routes.route("/active/submit/exam", methods=["POST"])
@routes.route("/active/submit/exam/<delay>", methods=["POST"])
@login_required
def submit_exam(delay:str = None):
    """
    View function for submitting the exam.
    """
    if not current_user.exam: return return_error(404, "No exam started.")
    if delay:
        time = scraper.submit_exam_delay(delay)
        if time == None: return return_error(500, "Error submitting exam.")
        return return_success(f"Exam will be submitted in {time} minutes.")
    else:
        result = scraper.submit_exam()
        if not result: return return_error(500, "Error submitting exam.")
        return return_data({"result_id": result.id})

@routes.route("/for_all", methods=["UPDATE"])
@login_required
def is_exam_for_all():
    examData = json.loads(request.data)
    if db_methods.update_exam_for_all(examData):
        return return_success("Exam updated.")
    return return_error(500, "Error updating exam.")
