from typing import List, Dict, Type
from .db import get_connection, init_db, ensure_columns
from .employee import Employee

class SQLiteStorage:
    def __init__(self, type_registry: Dict[str, Type[Employee]] = None):
        init_db()
        self.type_registry = type_registry or {}
        self._ensure_schema()

    def _get_all_fields(self):
        all_fields = {}
        for cls in self.type_registry.values():
            if hasattr(cls, "FIELDS"):
                for field_name, field_type in cls.FIELDS.items():
                    if field_name not in all_fields:
                        all_fields[field_name] = field_type
        return all_fields

    def _ensure_schema(self):
        conn = get_connection()
        try:
            all_fields = self._get_all_fields()
            ensure_columns(conn, all_fields)
            conn.commit()
        finally:
            conn.close()

    def save(self, items: List[Employee]):
        conn = get_connection()
        try:
            self._ensure_schema()
            conn.execute("DELETE FROM employees")
            all_fields = self._get_all_fields()
            field_names = sorted(all_fields.keys())
            
            for obj in items:
                data = self._object_to_row(obj)
                columns = ["type"] + field_names
                placeholders = ["?"] * len(columns)
                values = [data.get("type")] + [data.get(field) for field in field_names]
                
                query = f"INSERT INTO employees({', '.join(columns)}) VALUES({', '.join(placeholders)})"
                conn.execute(query, values)
            conn.commit()
        finally:
            conn.close()

    def load(self) -> List[Employee]:
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM employees ORDER BY id").fetchall()
            result = []
            for row in rows:
                obj = self._row_to_object(row)
                if obj is not None:
                    result.append(obj)
            return result
        finally:
            conn.close()

    def _row_to_object(self, row):
        if row is None:
            return None
        type_name = row["type"]
        cls = self.type_registry.get(type_name)
        if cls is None:
            return None

        obj = cls()
        for field_name in obj.FIELDS.keys():
            if field_name in row.keys():
                value = row[field_name]
                if obj.FIELDS[field_name] is bool:
                    setattr(obj, field_name, bool(value) if value is not None else False)
                elif obj.FIELDS[field_name] is int:
                    setattr(obj, field_name, int(value) if value is not None else 0)
                elif obj.FIELDS[field_name] is str:
                    setattr(obj, field_name, str(value) if value is not None else "")
                else:
                    setattr(obj, field_name, value)

        return obj

    def _object_to_row(self, obj: Employee):
        data = {"type": obj.__class__.__name__}

        for field_name in obj.FIELDS.keys():
            value = getattr(obj, field_name, None)
            if obj.FIELDS[field_name] is bool:
                data[field_name] = 1 if value else 0
            else:
                data[field_name] = value

        return data
