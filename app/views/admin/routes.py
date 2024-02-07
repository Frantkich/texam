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
