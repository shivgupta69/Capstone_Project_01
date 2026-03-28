from flask import Blueprint, flash, redirect, render_template, request, session

from app.services.task_service import (
    create_task_with_details,
    delete_task,
    get_user_category_counts,
    get_filtered_task_rows,
    get_user_stats,
    get_weekly_analytics,
    update_task_status,
)
from app.utils.helpers import login_required


task_bp = Blueprint("tasks", __name__)


@task_bp.route("/")
@login_required
def index():
    user_id = session["user_id"]
    filters = {
        "search": (request.args.get("search") or "").strip(),
        "category": (request.args.get("category") or "").strip(),
        "status": (request.args.get("status") or "").strip(),
        "due_filter": (request.args.get("due_filter") or "").strip(),
    }

    tasks = get_filtered_task_rows(
        user_id,
        search=filters["search"],
        category=filters["category"],
        status=filters["status"],
        due_filter=filters["due_filter"],
    )
    stats = get_user_stats(user_id)
    category_counts = get_user_category_counts(user_id)
    weekly_analytics = get_weekly_analytics(user_id)

    labels = [row[0] for row in stats]
    data = [row[1] for row in stats]

    return render_template(
        "dashboard.html",
        tasks=tasks,
        labels=labels,
        data=data,
        category_counts=category_counts,
        filters=filters,
        weekly_analytics=weekly_analytics,
    )


@task_bp.route("/add", methods=["POST"])
@login_required
def add_task():
    success, message, category = create_task_with_details(
        session["user_id"],
        request.form.get("task"),
        request.form.get("category"),
        request.form.get("duration"),
        request.form.get("due_date"),
        request.form.get("status") or "todo",
    )
    flash(message, category)
    return redirect("/")


@task_bp.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def remove_task(id):
    _, message, category = delete_task(id, session["user_id"])
    flash(message, category)
    return redirect("/")


@task_bp.route("/task/<int:id>/status", methods=["POST"])
@login_required
def change_task_status(id):
    _, message, category = update_task_status(
        id, session["user_id"], request.form.get("status")
    )
    flash(message, category)
    return redirect("/")
