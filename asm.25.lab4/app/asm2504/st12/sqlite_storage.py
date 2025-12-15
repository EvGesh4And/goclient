

import json
from typing import Dict, Iterable, List, Optional, Tuple



from .db import get_connection
from .base import BasePerson
from .registry import get_type


class SQLiteStorage:
    def get_all(self) -> List[BasePerson]:
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM students ORDER BY id").fetchall()
            result: List[BasePerson] = []
            for row in rows:
                obj = self._row_to_object(row)
                if obj is not None:
                    result.append(obj)
            return result
        finally:
            conn.close()

    def get_all_with_ids(self) -> List[Tuple[BasePerson, int]]:
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
            result: List[Tuple[BasePerson, int]] = []
            for row in rows:
                obj = self._row_to_object(row)
                if obj is not None:
                    result.append((obj, row["id"]))
            return result
        finally:
            conn.close()

    def add(self, obj: BasePerson) -> Optional[int]:
        return self._save_object(obj)

    def add_many(self, objects: Iterable[BasePerson]) -> int:
        inserted = 0
        for obj in objects:
            if self.add(obj):
                inserted += 1
        return inserted

    def get_by_id(self, item_id: int) -> Optional[BasePerson]:
        conn = get_connection()
        try:
            row = conn.execute("SELECT * FROM students WHERE id=?", (item_id,)).fetchone()
            return self._row_to_object(row) if row else None
        finally:
            conn.close()

    def update_by_id(self, item_id: int, obj: BasePerson) -> bool:
        return self._save_object(obj, item_id) is not None

    def remove_by_id(self, item_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.execute("DELETE FROM students WHERE id=?", (item_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def clear(self) -> int:
        conn = get_connection()
        try:
            cursor = conn.execute("DELETE FROM students")
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()

    def _row_to_object(self, row) -> Optional[BasePerson]:
        if row is None:
            return None
        cls = get_type(row["type"])
        if cls is None:
            return None

        obj = cls()
        raw_data = row["data"] if "data" in row.keys() else None
        payload: Dict[str, object]
        if raw_data:
            try:
                payload = json.loads(raw_data)
            except Exception:
                payload = {}
        else:
            payload = {}

        fields = getattr(obj, "FIELDS", {})
        if payload:
            for field_name in fields.keys():
                if field_name in payload:
                    setattr(obj, field_name, payload[field_name])
        else:
            row_keys = set(row.keys())
            for field_name, field_type in fields.items():
                source_name = field_name if field_name in row_keys else None
                if source_name is None and f"{field_name}_name" in row_keys:
                    source_name = f"{field_name}_name"
                if source_name is None:
                    continue
                value = row[source_name]
                if value is None:
                    continue
                if field_type is bool:
                    value = bool(value)
                setattr(obj, field_name, value)

        return obj

    def _object_to_payload(self, obj: BasePerson) -> Dict[str, object]:
        """Преобразовать объект в словарь для JSON-поля."""
        data: Dict[str, object] = {}
        for field_name in getattr(obj, "FIELDS", {}).keys():
            data[field_name] = getattr(obj, field_name, None)
        return data

    def _default_for_column(self, column_type: Optional[str]):
        """Получить значение по умолчанию для колонки."""
        column_type = (column_type or "").upper()
        if "INT" in column_type or "BOOL" in column_type:
            return 0
        if "REAL" in column_type or "FLOA" in column_type or "DOUB" in column_type:
            return 0.0
        return ""

    def _legacy_columns(self, conn) -> List[Dict[str, object]]:
        """Получить описание колонок таблицы (для обратной совместимости)."""
        try:
            cols = conn.execute("PRAGMA table_info(students)").fetchall()
        except Exception:
            return []
        return [{"name": col["name"], "type": col["type"]} for col in cols if col["name"] not in ("id", "type", "data")]

    def _extract_column_value(self, payload: Dict[str, object], column: Dict[str, object]):
        """Подобрать значение для колонки из payload."""
        col_name = column["name"]
        if col_name in payload:
            value = payload[col_name]
        elif col_name.endswith("_name"):
            fallback = col_name[:-5]
            value = payload.get(fallback)
        else:
            value = None
        if value is None:
            value = self._default_for_column(column.get("type"))
        if isinstance(value, bool):
            return 1 if value else 0
        return value

    def _save_object(self, obj: BasePerson, item_id: Optional[int] = None) -> Optional[int]:
        """Сохранить объект в БД."""
        payload = self._object_to_payload(obj)
        payload_json = json.dumps(payload, ensure_ascii=False)
        type_name = obj.__class__.__name__

        conn = get_connection()
        try:
            legacy_cols = self._legacy_columns(conn)

            if item_id is not None:
                set_parts = ["type = ?", "data = ?"]
                values = [type_name, payload_json]
                for column in legacy_cols:
                    set_parts.append(f"{column['name']} = ?")
                    values.append(self._extract_column_value(payload, column))
                values.append(item_id)
                sql = f"UPDATE students SET {', '.join(set_parts)} WHERE id=?"
                cursor = conn.execute(sql, tuple(values))
                conn.commit()
                return item_id if cursor.rowcount > 0 else None

            columns = ["type", "data"]
            values = [type_name, payload_json]
            for column in legacy_cols:
                columns.append(column["name"])
                values.append(self._extract_column_value(payload, column))
            placeholders = ", ".join(["?"] * len(columns))
            sql = f"INSERT INTO students({', '.join(columns)}) VALUES({placeholders})"
            cursor = conn.execute(sql, tuple(values))
            conn.commit()
            return cursor.lastrowid if cursor.rowcount > 0 else None
        finally:
            conn.close()

