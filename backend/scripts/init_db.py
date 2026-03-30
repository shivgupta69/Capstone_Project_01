#!/usr/bin/env python3
"""Initialize the database with required tables."""

from backend.app import create_app
from backend.app.utils.db import init_db


def main():
    """Create database tables."""
    app = create_app()
    with app.app_context():
        init_db()
    print("Database initialized successfully!")


if __name__ == "__main__":
    main()
