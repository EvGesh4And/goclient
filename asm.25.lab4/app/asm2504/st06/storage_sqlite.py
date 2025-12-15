# storage_sqlite.py
import sqlite3
import os
import pickle
from typing import Any, List, Optional, Tuple, Dict

def _ensure_data_dir() -> str:
    # считаем корень проекта как три уровня вверх от этого файла
    cur = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(cur, "..", "..", ".."))
    data_dir = os.path.join(project_root, "data", "asm2504", "st06")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

DB_DEFAULT = os.path.join(_ensure_data_dir(), "storage.db")

class SQLiteStorage:
    """
    Хранилище, работающее исключительно со словарями (rows).
    Интерфейс:
        - list_items() -> List[dict]
        - get_item(idx) -> dict | None  (idx — порядковый, OFFSET)
        - add_item(row: dict) -> lastrowid
        - update_item(idx, row: dict) -> bool
        - delete_item(idx) -> bool
        - clear()
        - save(filename) -> (ok, msg)  # экспорт в pickle (list of dicts)
        - load(filename) -> (ok, msg)  # импорт из pickle (dicts or objects)
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path if db_path else DB_DEFAULT
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()
        self.columns = self._get_columns()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._connect() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                manufacturer TEXT,
                model TEXT,
                price REAL,
                weight REAL,
                bayonet TEXT,
                sensor_size TEXT,
                megapixels REAL,
                focal_length TEXT,
                max_aperture TEXT,
                min_aperture TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            );
            """)
            conn.commit()

    def _get_columns(self) -> List[str]:
        with self._connect() as conn:
            cur = conn.execute("PRAGMA table_info(items);")
            cols = [row[1] for row in cur.fetchall()]
        return cols

    # --- CRUD (work with dicts) ---
    def list_items(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute("SELECT * FROM items ORDER BY id ASC;")
            rows = [dict(r) for r in cur.fetchall()]
        return rows

    def get_item(self, idx: int) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute("SELECT * FROM items ORDER BY id ASC LIMIT 1 OFFSET ?;", (idx,))
            row = cur.fetchone()
            return dict(row) if row else None

    def add_item(self, row: Dict[str, Any]) -> int:
        cols = [c for c in self.columns if c != "id"]
        placeholders = ", ".join(["?"] * len(cols))
        col_string = ", ".join(cols)
        values = [row.get(c) for c in cols]
        with self._connect() as conn:
            cur = conn.execute(f"INSERT INTO items ({col_string}) VALUES ({placeholders});", values)
            conn.commit()
            return cur.lastrowid

    def update_item(self, idx: int, row: Dict[str, Any]) -> bool:
        with self._connect() as conn:
            cur = conn.execute("SELECT id FROM items ORDER BY id ASC LIMIT 1 OFFSET ?;", (idx,))
            found = cur.fetchone()
            if not found:
                return False
            row_id = found["id"]
            cols = [c for c in self.columns if c != "id"]
            assignments = ", ".join([f"{c}=?" for c in cols])
            values = [row.get(c) for c in cols] + [row_id]
            conn.execute(f"UPDATE items SET {assignments} WHERE id = ?;", values)
            conn.commit()
            return True

    def delete_item(self, idx: int) -> bool:
        with self._connect() as conn:
            cur = conn.execute("SELECT id FROM items ORDER BY id ASC LIMIT 1 OFFSET ?;", (idx,))
            found = cur.fetchone()
            if not found:
                return False
            conn.execute("DELETE FROM items WHERE id = ?;", (found["id"],))
            conn.commit()
            return True

    def clear(self):
        with self._connect() as conn:
            conn.execute("DELETE FROM items;")
            conn.commit()

    # --- persistence (pickle) ---
    def save(self, filename: str) -> Tuple[bool, str]:
        fn = filename if filename.lower().endswith(".pickle") else filename + ".pickle"
        try:
            rows = self.list_items()
            with open(fn, "wb") as f:
                pickle.dump(rows, f)
            return True, f"Saved {len(rows)} items to '{fn}'."
        except Exception as e:
            return False, f"Error saving: {e}"

    def load(self, filename: str) -> Tuple[bool, str]:
        fn = filename if filename.lower().endswith(".pickle") else filename + ".pickle"
        if not os.path.exists(fn):
            return False, f"File '{fn}' not found."
        try:
            with open(fn, "rb") as f:
                data = pickle.load(f)
            count = 0
            with self._connect() as conn:
                for item in data:
                    if isinstance(item, dict):
                        cols = [c for c in self.columns if c != "id"]
                        placeholders = ", ".join(["?"] * len(cols))
                        params = [item.get(c) for c in cols]
                        conn.execute(f"INSERT INTO items ({', '.join(cols)}) VALUES ({placeholders});", params)
                        count += 1
                    else:
                        d = getattr(item, "__dict__", None)
                        if not isinstance(d, dict):
                            continue
                        d = dict(d)
                        d.pop("io", None)
                        cols = [c for c in self.columns if c != "id"]
                        params = [d.get(c) for c in cols]
                        placeholders = ", ".join(["?"] * len(cols))
                        conn.execute(f"INSERT INTO items ({', '.join(cols)}) VALUES ({placeholders});", params)
                        count += 1
                conn.commit()
            return True, f"Imported {count} items from '{fn}'."
        except Exception as e:
            return False, f"Error loading/importing: {e}"
