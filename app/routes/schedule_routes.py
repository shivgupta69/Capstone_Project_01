from flask import Blueprint, render_template, session

from app.services.schedule_service import generate_schedule
from app.services.task_service import get_user_task_rows
from app.utils.helpers import login_required


schedule_bp = Blueprint("schedule", __name__)


@schedule_bp.route("/schedule")
@login_required
def schedule_view():
    tasks = get_user_task_rows(session["user_id"])
    schedule = generate_schedule(tasks)
    return render_template("schedule.html", schedule=schedule)
