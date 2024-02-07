from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user
import json

from app.tools.helpers import (
    return_error,
    return_success,
    return_data,
    user_is_admin
)
import app.tools.db.methods as db_methods 
import app.views.exams.scraper as scraper


routes = Blueprint("admin", __name__, url_prefix="admin")


@routes.route("/")
@login_required
def index():
    if not user_is_admin(): return abort(403)
    return render_template("admin.html", exams=db_methods.get_exams())

@routes.route("/for_all", methods=["UPDATE"])
@login_required
def is_exam_for_all():
    if not user_is_admin(): return abort(403)
    examData = json.loads(request.data)
    if db_methods.update_exam_for_all(examData):
        return return_success("Exam updated.")
    return return_error(500, "Error updating exam.")

@routes.route("/create_user", methods=["POST"])
@login_required
def create_user():
    if not user_is_admin(): return abort(403)
    userData = json.loads(request.data)
    if db_methods.create_user(userData):
        return return_success("User created.")
    return return_error(500, "Error creating user.")
