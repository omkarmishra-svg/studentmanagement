import os
import sqlite3
from pathlib import Path
from flask import g

# Use /tmp on read-only platforms like Vercel
DEFAULT_DB_NAME = os.environ.get("DB_NAME", "students.db")
if os.environ.get("VERCEL"):
    DB_DIR = Path(os.environ.get("DB_DIR", "/tmp"))
else:
    DB_DIR = Path(__file__).resolve().parent

DB_PATH = DB_DIR / DEFAULT_DB_NAME


def ensure_db_dir():
    """Ensure the database directory exists and is writable."""
    DB_DIR.mkdir(parents=True, exist_ok=True)


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        ensure_db_dir()
        try:
            db = g._database = sqlite3.connect(DB_PATH, check_same_thread=False)
            db.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise
    return db


def init_db():
    try:
        ensure_db_dir()
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS students (
                roll INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                branch TEXT,
                mark1 REAL,
                mark2 REAL,
                mark3 REAL,
                mark4 REAL,
                mark5 REAL,
                percentage REAL,
                grade TEXT
            );
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
        raise