import os
import sqlite3

from flask import current_app, has_app_context


def get_db(flask_app=None):
    """Return a SQLite connection using app config when available."""
    if flask_app is not None:
        db_path = flask_app.config.get("DATABASE", "study.db")
    elif has_app_context():
        db_path = current_app.config.get("DATABASE", "study.db")
    else:
        db_path = os.getenv("DATABASE_PATH", "study.db")

    return sqlite3.connect(db_path)


def init_db(flask_app=None):
    """Create required tables if they do not already exist."""
    conn = get_db(flask_app)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task_name TEXT,
            category TEXT,
            duration INTEGER,
            due_date TEXT,
            status TEXT DEFAULT 'todo',
            estimated_hours REAL,
            scheduled_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS study_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            log_date TEXT NOT NULL,
            hours_studied REAL NOT NULL DEFAULT 0,
            tasks_completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )

    # Lightweight migration for existing databases created before due_date/status.
    cursor.execute("PRAGMA table_info(tasks)")
    existing_columns = {row[1] for row in cursor.fetchall()}

    if "due_date" not in existing_columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT")

    if "status" not in existing_columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN status TEXT DEFAULT 'todo'")

    if "estimated_hours" not in existing_columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN estimated_hours REAL")

    if "scheduled_date" not in existing_columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN scheduled_date TEXT")

    cursor.execute(
        "UPDATE tasks SET status='todo' WHERE status IS NULL OR TRIM(status)=''"
    )
    cursor.execute(
        "UPDATE tasks SET estimated_hours=duration WHERE estimated_hours IS NULL"
    )

    conn.commit()
    conn.close()
