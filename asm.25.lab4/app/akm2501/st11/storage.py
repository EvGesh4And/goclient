import os
import pickle
import sqlite3
import uuid
import json
from typing import Callable, Optional, Type, Dict, Tuple, Iterable, List
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = LAB_ROOT / "data" / "akm2501" / "st11"
DATA_DIR.mkdir(parents=True, exist_ok=True)
PICKLE_PATH = DATA_DIR / "animals.db"
SQLITE_PATH = DATA_DIR / "animals.sqlite3"

class StorageStrategy:
    def add(self, item):
        raise NotImplementedError
    def get_all(self):
        raise NotImplementedError
    def get_by_id(self, item_id):
        raise NotImplementedError
    def update_by_id(self, item_id, item):
        raise NotImplementedError
    def delete_by_id(self, item_id):
        raise NotImplementedError
    def clear(self):
        raise NotImplementedError
    def save(self, filename):
        raise NotImplementedError
    def load(self, filename):
        raise NotImplementedError

class PickleStorage(StorageStrategy):
    def __init__(self, path: Path | None = None):
        self._items = {}
        self.path = Path(path or PICKLE_PATH)

    def add(self, item):
        if not item.id:
            item.id = str(uuid.uuid4())
        self._items[item.id] = item

    def get_all(self):
        return list(self._items.values())

    def get_by_id(self, item_id):
        return self._items.get(item_id)

    def update_by_id(self, item_id, item):
        if item_id in self._items:
            item.id = item_id
            self._items[item_id] = item

    def delete_by_id(self, item_id):
        if item_id in self._items:
            del self._items[item_id]

    def clear(self):
        self._items.clear()

    def save(self, filename):
        if filename:
            self.path = Path(filename)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, 'wb') as f:
            pickle.dump(self._items, f)

    def load(self, filename):
        if filename:
            self.path = Path(filename)
        try:
            with open(self.path, 'rb') as f:
                self._items = pickle.load(f)
        except FileNotFoundError:
            self._items = {}

class SQLiteStorage(StorageStrategy):
    def __init__(self, db_path: Path | None = None, type_resolver: Optional[Callable[[str], Optional[Type]]] = None):
        self.db_path = Path(db_path or SQLITE_PATH)
        self._type_resolver = type_resolver or (lambda _n: None)
        self.init_db()
        self.import_from_pickle()
    
    def init_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS animals (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    data TEXT
                )
            ''')
            
            try:
                cols = cursor.execute("PRAGMA table_info(animals)").fetchall()
                names = {c[1] for c in cols}
                if "type" not in names:
                    cursor.execute("ALTER TABLE animals ADD COLUMN type TEXT")
                if "data" not in names:
                    cursor.execute("ALTER TABLE animals ADD COLUMN data TEXT")
            except Exception:
                pass
            conn.commit()
    
    def import_from_pickle(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM animals")
                count = cursor.fetchone()[0]
                if count == 0 and PICKLE_PATH.exists():
                    with open(PICKLE_PATH, 'rb') as f:
                        pickle_data = pickle.load(f)
                    for _, animal in pickle_data.items():
                        self._insert_object(animal.id or str(uuid.uuid4()), animal)
        except Exception:
            pass
    
    def _insert_object(self, obj_id: str, obj) -> None:
        type_name = obj.__class__.__name__
        fields = getattr(obj, "fields", lambda: [])()
        data: Dict[str, object] = {}
        for field in fields:
            data[field] = getattr(obj, field, None)
        payload = json.dumps(data, ensure_ascii=False)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO animals(id, type, data) VALUES(?, ?, ?)",
                (obj_id, type_name, payload),
            )
            conn.commit()
    
    def add(self, item):
        if not getattr(item, "id", None):
            item.id = str(uuid.uuid4())
        self._insert_object(item.id, item)
        return item.id
    
    def get_all(self):
        result = []
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM animals ORDER BY rowid")
            for row in cursor:
                obj = self._row_to_object(row)
                if obj:
                    result.append(obj)
        return result

    def get_all_with_ids(self) -> List[Tuple[str, object]]:
        result: List[Tuple[str, object]] = []
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM animals ORDER BY rowid")
            for row in cursor:
                obj = self._row_to_object(row)
                if obj:
                    result.append((row["id"], obj))
        return result
    
    def _row_to_object(self, row):
        type_name = row["type"] if "type" in row.keys() else None
        cls = self._type_resolver(type_name) if type_name else None
        if cls is None:
            return None
        obj = cls()
        obj.id = row["id"]
        raw = row["data"] if "data" in row.keys() else None
        data = {}
        if raw:
            try:
                data = json.loads(raw)
            except Exception:
                data = {}
        fields = getattr(obj, "fields", lambda: [])()
        for field in fields:
            if field in data:
                setattr(obj, field, data[field])
        return obj
    
    def get_by_id(self, item_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM animals WHERE id = ?", (item_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_object(row)
        return None
    
    def update_by_id(self, item_id, item):
        type_name = item.__class__.__name__
        fields = getattr(item, "fields", lambda: [])()
        data: Dict[str, object] = {}
        for field in fields:
            data[field] = getattr(item, field, None)
        payload = json.dumps(data, ensure_ascii=False)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE animals SET type=?, data=? WHERE id=?",
                (type_name, payload, item_id),
            )
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_by_id(self, item_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM animals WHERE id = ?", (item_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def clear(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM animals")
            conn.commit()
            return cursor.rowcount
    
    def save(self, filename):
        pass
    
    def load(self, filename):
        pass