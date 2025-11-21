import sqlite3
from flask import g
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "students.db")

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        try:
            db = g._database = sqlite3.connect(DB_PATH, check_same_thread=False)
            db.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise
    return db

def init_db():
    try:
        # Create directory if it doesn't exist
        db_dir = os.path.dirname(DB_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        # Connect and create table if it doesn't exist
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        c = conn.cursor()
        
        # Check if table exists
        c.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='students'
        """)
        
        if not c.fetchone():
            # Table doesn't exist, create it
            c.execute("""
                CREATE TABLE students (
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
            print("Database table created successfully")
        else:
            print("Database table already exists")
        
        conn.close()
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
        raise