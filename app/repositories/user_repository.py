import sqlite3

from app.utils.db import get_db


def insert_user(username, hashed_password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password),
    )
    conn.commit()
    conn.close()


def fetch_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()
    return row


def is_duplicate_username_error(exc):
    return isinstance(exc, sqlite3.IntegrityError)

