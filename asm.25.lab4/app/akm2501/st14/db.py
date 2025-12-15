import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
AKM_DIR = os.path.join(DATA_DIR, "akm2501")
ST14_DIR = os.path.join(AKM_DIR, "st14")
os.makedirs(ST14_DIR, exist_ok=True)

DB_PATH = os.path.join(ST14_DIR, "st14.sqlite3")


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL
            )
            """
        )
        conn.commit()


def ensure_columns(conn, field_types):
    existing_cols = {row["name"] for row in conn.execute("PRAGMA table_info(employees)").fetchall()}
    
    for field_name, field_type in field_types.items():
        if field_name in existing_cols:
            continue
        
        if not field_name.replace("_", "").isalnum():
            continue
        
        sql_type = "TEXT"
        if field_type is int:
            sql_type = "INTEGER"
        elif field_type is float:
            sql_type = "REAL"
        elif field_type is bool:
            sql_type = "INTEGER"
        
        try:
            conn.execute(f"ALTER TABLE employees ADD COLUMN {field_name} {sql_type}")
        except sqlite3.OperationalError:
            pass
