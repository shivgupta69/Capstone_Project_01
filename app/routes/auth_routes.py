from datetime import datetime, timezone

from flask import Blueprint, flash, redirect, render_template, request, session

from app.services.auth_service import authenticate_user, register_user
from app.utils.helpers import login_required


auth_bp = Blueprint("auth", __name__)


def _start_user_session(user_id):
    # Reset session data on login to reduce fixation risk.
    session.clear()
    session["user_id"] = user_id
    session["authenticated_at"] = datetime.now(timezone.utc).isoformat()
    session.permanent = True


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        success, message, category = register_user(
            request.form.get("username"), request.form.get("password")
        )
        if success:
            flash(message, category)
            return redirect("/login")

        flash(message, category)
        return redirect("/register")

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        success, user_id, message, category = authenticate_user(
            request.form.get("username"), request.form.get("password")
        )

        if success:
            _start_user_session(user_id)
            flash("Welcome back!", "success")
            return redirect("/")

        flash(message, category)

    return render_template("login.html")


@auth_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    session.clear()
    flash("You have been logged out safely.", "success")
    return redirect("/login")
