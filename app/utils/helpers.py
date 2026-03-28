from functools import wraps

from flask import flash, redirect, session


def login_required(view_func):
    """Simple auth guard for routes that require a signed-in user."""

    @wraps(view_func)
    def wrapped(*args, **kwargs):
        user_id = session.get("user_id")
        if not isinstance(user_id, int) or user_id <= 0:
            session.clear()
            flash("Please log in to continue.", "error")
            return redirect("/login")
        return view_func(*args, **kwargs)

    return wrapped
