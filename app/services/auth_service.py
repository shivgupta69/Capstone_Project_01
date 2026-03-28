import sqlite3
import re

from app.models.user_model import User
from app.repositories.user_repository import (
    fetch_user_by_username,
    insert_user,
    is_duplicate_username_error,
)
from app.utils.security import hash_password, verify_password


USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+$")


def register_user(username, password):
    username = (username or "").strip()
    password = (password or "").strip()

    if not username or not password:
        return False, "Username and password cannot be empty.", "error"

    if len(username) > 50:
        return False, "Username must be 50 characters or fewer.", "error"

    if not USERNAME_PATTERN.fullmatch(username):
        return (
            False,
            "Username can only include letters, numbers, dot, underscore, and dash.",
            "error",
        )

    if len(password) < 8:
        return False, "Password must be at least 8 characters.", "error"

    hashed_password = hash_password(password)

    try:
        insert_user(username, hashed_password)
    except sqlite3.Error as exc:
        if is_duplicate_username_error(exc):
            return False, "Username already exists. Please choose another.", "error"

        return False, "Unable to register right now. Please try again.", "error"
    except Exception:
        # Defensive catch-all to avoid exposing internals.
        return False, "Unable to register right now. Please try again.", "error"

    return True, "Registration successful! Please login.", "success"


def authenticate_user(username, password):
    username = (username or "").strip()
    password = (password or "").strip()

    if not username or not password:
        return False, None, "Username and password cannot be empty.", "error"

    try:
        row = fetch_user_by_username(username)
    except sqlite3.Error:
        return False, None, "Unable to login right now. Please try again.", "error"
    except Exception:
        return False, None, "Unable to login right now. Please try again.", "error"

    user = User.from_row(row)
    if user and verify_password(user.password, password):
        return True, user.id, None, None

    return False, None, "Invalid username or password.", "error"
