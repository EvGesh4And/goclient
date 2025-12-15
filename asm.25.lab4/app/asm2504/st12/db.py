import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
ASM_DIR = os.path.join(DATA_DIR, "asm2504")
ST12_DIR = os.path.join(ASM_DIR, "st12")

try:
    os.makedirs(ST12_DIR, exist_ok=True)
except (OSError, PermissionError):
    pass  # Директория будет создана при первом использовании

DB_PATH = os.path.join(ST12_DIR, "st12.sqlite3")


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                group_name TEXT,
                record_book TEXT,
                avg_grade REAL,
                phone TEXT,
                duties TEXT,
                union_member INTEGER,
                events_count INTEGER,
                data TEXT
            )
            """
        )
        try:
            cols = conn.execute("PRAGMA table_info(students)").fetchall()
            col_names = {c["name"] for c in cols}
            if "data" not in col_names:
                conn.execute("ALTER TABLE students ADD COLUMN data TEXT")
        except Exception:
            pass
        conn.commit()

