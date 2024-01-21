from flask import Blueprint, render_template
from flask_login import login_required

routes = Blueprint("frontend", __name__, url_prefix="")


@routes.route("/")
@login_required
def index():
    return render_template("index.html")

@routes.route("/export")
@login_required
def export():
    import app.tools.export as export
    export.export_questions()
    return "Export done."