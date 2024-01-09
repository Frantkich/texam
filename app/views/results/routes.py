from flask import Blueprint, render_template
from flask_login import login_required
import json

from app.tools.db.methods import get_user_results


routes = Blueprint("results", __name__, url_prefix="/results")


@routes.route("/")
@login_required
def index():
    return render_template("results.html", results=get_user_results())

@routes.route("/<int:id>")
@login_required
def result(id):
    result = get_user_results(id)
    result.detail_score = json.loads(result.detail_score)
    result.submitted_questions = json.loads(result.submitted_questions)
    return render_template("result.html", result=result)
