import sqlite3

from app.models.task_model import Task
from app.repositories.task_repository import (
    delete_task_for_user,
    fetch_category_counts,
    fetch_distinct_categories,
    fetch_filtered_tasks,
    fetch_task_by_id_for_user,
    fetch_stats_by_category,
    fetch_task_columns,
    fetch_tasks_by_user_id,
    fetch_weekly_analytics,
    insert_task,
    update_task_status_for_user,
)
from app.services.analytics_service import track_completion_delta
from app.services.scheduling_service import schedule_user_tasks

VALID_TASK_STATUSES = {"todo", "in-progress", "done"}


def _is_valid_id(value):
    return isinstance(value, int) and value > 0


def get_user_tasks(user_id):
    if not _is_valid_id(user_id):
        return []

    try:
        rows = fetch_tasks_by_user_id(user_id)
    except sqlite3.Error:
        return []
    except Exception:
        return []

    return [Task.from_row(row) for row in rows]


def get_user_task_rows(user_id):
    """Return raw rows to keep templates backward-compatible with index access."""
    if not _is_valid_id(user_id):
        return []

    try:
        return fetch_tasks_by_user_id(user_id)
    except sqlite3.Error:
        return []
    except Exception:
        return []


def get_filtered_task_rows(user_id, search="", category="", status="", due_filter=""):
    if not _is_valid_id(user_id):
        return []

    if status and status not in VALID_TASK_STATUSES:
        status = ""

    if due_filter not in {"", "today", "this-week", "overdue"}:
        due_filter = ""

    try:
        return fetch_filtered_tasks(
            user_id, search=search, category=category, status=status, due_filter=due_filter
        )
    except sqlite3.Error:
        return []
    except Exception:
        return []


def get_user_categories(user_id):
    if not _is_valid_id(user_id):
        return []

    try:
        rows = fetch_distinct_categories(user_id)
    except sqlite3.Error:
        return []
    except Exception:
        return []

    return [row[0] for row in rows]


def get_user_category_counts(user_id):
    if not _is_valid_id(user_id):
        return []

    try:
        rows = fetch_category_counts(user_id)
    except sqlite3.Error:
        return []
    except Exception:
        return []

    return [{"name": row[0], "count": row[1]} for row in rows]


def get_user_stats(user_id):
    if not _is_valid_id(user_id):
        return []

    try:
        return fetch_stats_by_category(user_id)
    except sqlite3.Error:
        return []
    except Exception:
        return []


def create_task(user_id, task_name, category, duration_value):
    task_name = (task_name or "").strip()
    category = (category or "").strip()

    if not task_name or not category:
        return False, "Task name and category cannot be empty.", "error"

    try:
        duration = int(duration_value)
        if duration < 1:
            raise ValueError
    except (TypeError, ValueError):
        return False, "Duration must be a whole number of at least 1.", "error"

    if not _is_valid_id(user_id):
        return False, "Invalid user context.", "error"

    try:
        insert_task(
            user_id=user_id,
            task_name=task_name,
            category=category,
            duration=duration,
            due_date=None,
            status="todo",
            estimated_hours=duration,
            scheduled_date=None,
        )
        schedule_user_tasks(user_id)
    except sqlite3.Error:
        return False, "Unable to add task right now. Please try again.", "error"
    except Exception:
        return False, "Unable to add task right now. Please try again.", "error"

    return True, "Task added", "success"


def create_task_with_details(
    user_id, task_name, category, duration_value, due_date=None, status="todo"
):
    task_name = (task_name or "").strip()
    category = (category or "").strip()
    due_date = (due_date or "").strip() or None
    status = (status or "todo").strip()

    if not task_name or not category:
        return False, "Task name and category cannot be empty.", "error"

    if status not in VALID_TASK_STATUSES:
        return False, "Invalid task status.", "error"

    try:
        duration = int(duration_value)
        if duration < 1:
            raise ValueError
    except (TypeError, ValueError):
        return False, "Duration must be a whole number of at least 1.", "error"

    if not _is_valid_id(user_id):
        return False, "Invalid user context.", "error"

    try:
        insert_task(
            user_id=user_id,
            task_name=task_name,
            category=category,
            duration=duration,
            due_date=due_date,
            status=status,
            estimated_hours=duration,
            scheduled_date=None,
        )
        track_completion_delta(user_id, "todo", status, duration)
        schedule_user_tasks(user_id)
    except sqlite3.Error:
        return False, "Unable to add task right now. Please try again.", "error"
    except Exception:
        return False, "Unable to add task right now. Please try again.", "error"

    return True, "Task added", "success"


def delete_task(task_id, user_id):
    if not _is_valid_id(task_id) or not _is_valid_id(user_id):
        return False, "Task not found or already removed.", "error"

    try:
        deleted_count = delete_task_for_user(task_id, user_id)
        if deleted_count:
            schedule_user_tasks(user_id)
    except sqlite3.Error:
        return False, "Unable to delete task right now. Please try again.", "error"
    except Exception:
        return False, "Unable to delete task right now. Please try again.", "error"

    if deleted_count:
        return True, "Task deleted", "success"

    return False, "Task not found or already removed.", "error"


def update_task_status(task_id, user_id, status):
    status = (status or "").strip()
    if status not in VALID_TASK_STATUSES:
        return False, "Invalid task status.", "error"

    if not _is_valid_id(task_id) or not _is_valid_id(user_id):
        return False, "Task not found or already removed.", "error"

    try:
        existing_task = fetch_task_by_id_for_user(task_id, user_id)
        if not existing_task:
            return False, "Task not found or already removed.", "error"

        previous_status = existing_task[6] if len(existing_task) > 6 and existing_task[6] else "todo"
        duration = existing_task[4] if len(existing_task) > 4 else 0

        updated_count = update_task_status_for_user(task_id, user_id, status)
        if updated_count:
            track_completion_delta(user_id, previous_status, status, duration)
            schedule_user_tasks(user_id)
    except sqlite3.Error:
        return False, "Unable to update task status right now. Please try again.", "error"
    except Exception:
        return False, "Unable to update task status right now. Please try again.", "error"

    if updated_count:
        return True, "Task status updated", "success"

    return False, "Task not found or already removed.", "error"


def get_weekly_analytics(user_id):
    if not _is_valid_id(user_id):
        return {"planned_hours": 0, "completed_tasks": 0, "due_tasks": 0}

    try:
        task_columns = fetch_task_columns()
    except sqlite3.Error:
        return {"planned_hours": 0, "completed_tasks": 0, "due_tasks": 0}
    except Exception:
        return {"planned_hours": 0, "completed_tasks": 0, "due_tasks": 0}

    if "due_date" not in task_columns or "status" not in task_columns:
        return {"planned_hours": 0, "completed_tasks": 0, "due_tasks": 0}

    try:
        row = fetch_weekly_analytics(user_id)
    except sqlite3.Error:
        return {"planned_hours": 0, "completed_tasks": 0, "due_tasks": 0}
    except Exception:
        return {"planned_hours": 0, "completed_tasks": 0, "due_tasks": 0}

    return {
        "planned_hours": row[0] if row else 0,
        "completed_tasks": row[1] if row else 0,
        "due_tasks": row[2] if row else 0,
    }
