import sqlite3
import os
from contextlib import contextmanager

# Путь к БД в подкаталоге data
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data", "asm2504", "st01")
DB_PATH = os.path.join(DB_DIR, "cardex.db")

os.makedirs(DB_DIR, exist_ok=True)


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                name TEXT NOT NULL UNIQUE,
                age INTEGER NOT NULL CHECK (age >= 16 AND age <= 100),
                group_role TEXT,
                union_activity TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


def add_entity(data):
    with get_db() as conn:
        cursor = conn.execute(
            """
            INSERT OR IGNORE INTO entities (type, name, age, group_role, union_activity)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                data["type"],
                data["name"],
                data["age"],
                data.get("group_role", ""),
                data.get("union_activity", ""),
            ),
        )
        conn.commit()
        return cursor.lastrowid


def get_all_entities():
    with get_db() as conn:
        return conn.execute(
            """
            SELECT * FROM entities ORDER BY id ASC
        """
        ).fetchall()

def get_entity_by_id(entity_id):
    with get_db() as conn:
        return conn.execute(
            """
            SELECT * FROM entities WHERE id = ?
        """, (entity_id,)
        ).fetchone()

def update_entity(entity_id, data):
    with get_db() as conn:
        conn.execute(
            """
            UPDATE entities 
            SET name = ?, age = ?, group_role = ?, union_activity = ?
            WHERE id = ?
        """,
            (
                data["name"],
                data["age"],
                data.get("group_role", ""),
                data.get("union_activity", ""),
                entity_id,
            ),
        )
        conn.commit()


def delete_entity(entity_id):
    with get_db() as conn:
        conn.execute("DELETE FROM entities WHERE id = ?", (entity_id,))
        conn.commit()


def clear_all():
    with get_db() as conn:
        conn.execute("DELETE FROM entities")
        conn.commit()
