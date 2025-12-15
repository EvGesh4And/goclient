import sqlite3
from typing import List, Any, Type, Optional
from pathlib import Path
from contextlib import contextmanager

class SQLiteStorage:
    def __init__(self,
                 classes: Optional[List[Type]] = None,
                 base_dir: Optional[Path] = None,
                 items: Optional[List[Any]] = None):
        self.classes = list(classes) if classes is not None else []
        self.base_dir = Path(base_dir) if base_dir is not None else Path(".")
        self.db_path = self.base_dir / "storage.db"
        self._ensure_db_dir()
        self._table_names_raw = {c: getattr(c, "__name__", "tbl").strip() for c in self.classes}
        self._table_names = {c: self._safe_table_name(c) for c in self.classes}
        self._ensure_tables()
        if items is not None:
            self._replace_db_with_items(items)

    def _ensure_db_dir(self):
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _safe_table_name(self, cls: Type) -> str:
        name = getattr(cls, "__name__", "tbl").strip()
        safe = "".join(ch if (ch.isalnum() or ch == "_") else "_" for ch in name)
        return safe

    def _quote_ident(self, name: str) -> str:
        safe = "".join(ch if (ch.isalnum() or ch == "_") else "_" for ch in name)
        return f'"{safe}"'

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(str(self.db_path))
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _ensure_tables(self):
        with self._connect() as conn:
            cur = conn.cursor()
            for cls in self.classes:
                tbl = self._table_names[cls]
                cols = []
                for fname in cls.fields.keys():
                    cols.append(f"{self._quote_ident(fname)} TEXT")
                sql = f"CREATE TABLE IF NOT EXISTS {self._quote_ident(tbl)} ({', '.join(cols)});"
                cur.execute(sql)

    def _row_to_obj(self, cls: Type, row: sqlite3.Row) -> Any:
        obj = cls()
        obj._data = {}
        for key in cls.fields.keys():
            obj._data[key] = row[key] if key in row.keys() else None
        return obj

    def _replace_db_with_items(self, items: List[Any]):
        with self._connect() as conn:
            cur = conn.cursor()
            for cls in self.classes:
                tbl = self._table_names[cls]
                cur.execute(f"DELETE FROM {self._quote_ident(tbl)}")
            for obj in items:
                cls = obj.__class__
                tbl = self._table_names.get(cls)
                if tbl is None:
                    continue
                cols = list(cls.fields.keys())
                if cols:
                    col_list = ", ".join(self._quote_ident(c) for c in cols)
                    placeholders = ", ".join(f":{c}" for c in cols)
                    params = {c: (None if obj._data.get(c) is None else obj._data.get(c)) for c in cols}
                    cur.execute(f"INSERT INTO {self._quote_ident(tbl)} ({col_list}) VALUES ({placeholders})", params)
                else:
                    cur.execute(f"INSERT INTO {self._quote_ident(tbl)} DEFAULT VALUES")

    def add(self, obj: Any):
        cls = obj.__class__
        tbl = self._table_names.get(cls)
        if tbl is None:
            raise ValueError("Unknown class for storage")
        cols = list(cls.fields.keys())
        with self._connect() as conn:
            cur = conn.cursor()
            if cols:
                col_list = ", ".join(self._quote_ident(c) for c in cols)
                placeholders = ", ".join(f":{c}" for c in cols)
                params = {c: (None if obj._data.get(c) is None else obj._data.get(c)) for c in cols}
                cur.execute(f"INSERT INTO {self._quote_ident(tbl)} ({col_list}) VALUES ({placeholders})", params)
                return cur.lastrowid
            else:
                cur.execute(f"INSERT INTO {self._quote_ident(tbl)} DEFAULT VALUES")
                return cur.lastrowid

    def list(self) -> List[Any]:
        results: List[Any] = []
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            for cls in self.classes:
                tbl = self._table_names[cls]
                col_names = ", ".join(self._quote_ident(c) for c in cls.fields.keys()) if cls.fields else ""
                select_cols = f"ROWID, {col_names}" if col_names else "ROWID"
                sql = f"SELECT {select_cols} FROM {self._quote_ident(tbl)} ORDER BY ROWID"
                cur.execute(sql)
                rows = cur.fetchall()
                for r in rows:
                    obj = self._row_to_obj(cls, r)
                    obj._rowid = r["ROWID"]
                    results.append(obj)
        return results

    def remove(self, index: int) -> Any:
        rows = []
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            for cls in self.classes:
                tbl = self._table_names[cls]
                col_names = ", ".join(self._quote_ident(c) for c in cls.fields.keys()) if cls.fields else ""
                select_cols = f"ROWID, {col_names}" if col_names else "ROWID"
                sql = f"SELECT {select_cols} FROM {self._quote_ident(tbl)} ORDER BY ROWID"
                cur.execute(sql)
                fetched = cur.fetchall()
                for r in fetched:
                    rows.append((cls, r))
            if not (0 <= index < len(rows)):
                raise IndexError("index out of range")
            cls, row = rows[index]
            tbl = self._table_names[cls]
            cur.execute(f"DELETE FROM {self._quote_ident(tbl)} WHERE ROWID = :rowid", {"rowid": row["ROWID"]})
            obj = self._row_to_obj(cls, row)
            obj._rowid = row["ROWID"]
            return obj

    def update(self, index: int, obj: Any):
        rows = []
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            for cls in self.classes:
                tbl = self._table_names[cls]
                col_names = ", ".join(self._quote_ident(c) for c in cls.fields.keys()) if cls.fields else ""
                select_cols = f"ROWID, {col_names}" if col_names else "ROWID"
                sql = f"SELECT {select_cols} FROM {self._quote_ident(tbl)} ORDER BY ROWID"
                cur.execute(sql)
                fetched = cur.fetchall()
                for r in fetched:
                    rows.append((cls, r))
            total = len(rows)
            cls = obj.__class__
            tbl = self._table_names.get(cls)
            if tbl is None:
                raise ValueError("Unknown class for storage")
            cols = list(cls.fields.keys())

            if index == total:
                if cols:
                    col_list = ", ".join(self._quote_ident(c) for c in cols)
                    placeholders = ", ".join(f":{c}" for c in cols)
                    params = {c: (None if obj._data.get(c) is None else obj._data.get(c)) for c in cols}
                    cur.execute(f"INSERT INTO {self._quote_ident(tbl)} ({col_list}) VALUES ({placeholders})", params)
                    return cur.lastrowid
                else:
                    cur.execute(f"INSERT INTO {self._quote_ident(tbl)} DEFAULT VALUES")
                    return cur.lastrowid
            if not (0 <= index < total):
                raise IndexError("index out of range")
            target_cls, row = rows[index]
            if target_cls is not cls:
                raise ValueError("Cannot update: index refers to a different class")
            rowid = row["ROWID"]
            if cols:
                set_clause = ", ".join(f"{self._quote_ident(c)} = :{c}" for c in cols)
                params = {c: (None if obj._data.get(c) is None else obj._data.get(c)) for c in cols}
                params["rowid"] = rowid
                cur.execute(f"UPDATE {self._quote_ident(tbl)} SET {set_clause} WHERE ROWID = :rowid", params)
                return rowid
            else:
                cur.execute(f"SELECT ROWID FROM {self._quote_ident(tbl)} WHERE ROWID = :rowid", {"rowid": rowid})
                if cur.fetchone() is None:
                    cur.execute(f"INSERT INTO {self._quote_ident(tbl)} DEFAULT VALUES")
                    return cur.lastrowid
                return rowid

    def clear(self):
        with self._connect() as conn:
            cur = conn.cursor()
            for cls in self.classes:
                tbl_quoted = self._table_names[cls]
                tbl_raw = self._table_names_raw[cls]
                cur.execute(f"DELETE FROM {self._quote_ident(tbl_quoted)}")
                try:
                    cur.execute("DELETE FROM sqlite_sequence WHERE name = :tbl", {"tbl": tbl_raw})
                except sqlite3.OperationalError:
                    pass

    def _import_from_db(self, src_path: Path):
        src_path = Path(src_path)
        if not src_path.exists():
            raise FileNotFoundError(f"No such database file: {src_path}")
        with sqlite3.connect(str(src_path)) as src_conn, self._connect() as dst_conn:
            src_conn.row_factory = sqlite3.Row
            src_cur = src_conn.cursor()
            dst_cur = dst_conn.cursor()
            for cls in self.classes:
                tbl = self._table_names[cls]
                col_names = [c for c in cls.fields.keys()]
                if not col_names:
                    try:
                        src_cur.execute(f"SELECT ROWID FROM {self._quote_ident(tbl)}")
                    except sqlite3.OperationalError:
                        continue
                    rows = src_cur.fetchall()
                    dst_cur.execute(f"DELETE FROM {self._quote_ident(tbl)}")
                    if not rows:
                        continue
                    for _ in rows:
                        dst_cur.execute(f"INSERT INTO {self._quote_ident(tbl)} DEFAULT VALUES")
                    continue

                cols_quoted = ", ".join(self._quote_ident(c) for c in col_names)
                src_sql = f"SELECT {cols_quoted} FROM {self._quote_ident(tbl)}"
                try:
                    src_cur.execute(src_sql)
                except sqlite3.OperationalError:
                    continue
                rows = src_cur.fetchall()
                dst_cur.execute(f"DELETE FROM {self._quote_ident(tbl)}")
                if not rows:
                    continue
                placeholders = ", ".join("?" for _ in col_names)
                insert_sql = f"INSERT INTO {self._quote_ident(tbl)} ({cols_quoted}) VALUES ({placeholders})"
                to_insert = []
                for r in rows:
                    row_vals = [r[c] if c in r.keys() else None for c in col_names]
                    to_insert.append(tuple(None if v is None else v for v in row_vals))
                dst_cur.executemany(insert_sql, to_insert)

    def load(self, filename: str):
        name = Path(filename).name
        src = self.base_dir / name
        if not src.exists():
            raise FileNotFoundError(f"Такой базы данных не существует: {src}")
        self.db_path.write_bytes(src.read_bytes())
        self._import_from_db(self.db_path)

    def save(self, filename: str):
        name = Path(filename).name
        dest = self.base_dir / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            self._ensure_tables()
        dest.write_bytes(self.db_path.read_bytes())
