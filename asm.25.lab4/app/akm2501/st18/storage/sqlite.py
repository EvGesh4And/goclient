import shutil
import sqlite3
from pathlib import Path
from typing import Dict, Optional

from app.akm2501.st18.models import Employee, Item, Student


class SqliteStorage:
    def __init__(self):
        data_directory = Path(__file__).resolve().parents[4] / "data" / "akm2501" / "st18"
        data_directory.mkdir(parents=True, exist_ok=True)

        self.__data_base_file = data_directory / "data.sqlite"

        self.__ensure_schema()

    def load(self):
        items = self.get_items()
        max_id = max(items.keys()) if items else 0
        return max_id, items

    def store(self, max_id: int, items: Dict[int, Item]):
        pass

    def get_items(self) -> Dict[int, Item]:
        with sqlite3.connect(self.__data_base_file) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM items ORDER BY id")
            rows = cursor.fetchall()

        items = {}
        for row in rows:
            item = self.__convert_row_to_item(row)
            items[item.id] = item

        return items

    def get(self, id: int) -> Optional[Item]:
        with sqlite3.connect(self.__data_base_file) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM items WHERE id = ?", (id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return self.__convert_row_to_item(row)

    def add(self, item: Item) -> int:
        data = item.get_data()
        item_type = self.__get_item_type_name(item)

        fields = ['"type"']
        values_placeholders = ["?"]
        values = [item_type]

        for field, value in data.items():
            if field == "id":
                continue
            fields.append(f'"{field}"')
            values_placeholders.append("?")
            values.append(value)

        query = f"INSERT INTO items({', '.join(fields)}) VALUES({', '.join(values_placeholders)})"

        with sqlite3.connect(self.__data_base_file) as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            return cursor.lastrowid

    def update(self, item: Item) -> None:
        data = item.get_data()

        updates = []
        values = []

        for field, value in data.items():
            if field == "id":
                continue
            updates.append(f'"{field}" = ?')
            values.append(value)

        values.append(data["id"])

        query = f'UPDATE items SET {", ".join(updates)} WHERE "id" = ?'

        with sqlite3.connect(self.__data_base_file) as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

    def delete(self, id: int) -> bool:
        with sqlite3.connect(self.__data_base_file) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM items WHERE id = ?", (id,))
            conn.commit()
            return cursor.rowcount == 1

    def clear(self) -> bool:
        with sqlite3.connect(self.__data_base_file) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM items")
            conn.commit()
            return True

    def __ensure_schema(self):
        query = '''
            CREATE TABLE IF NOT EXISTS items (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "type" TEXT NOT NULL,
                "created_at" TEXT NOT NULL,
                "name" TEXT,
                "age" INTEGER,
                "group_name" TEXT,
                "position" TEXT
            )
        '''
        with sqlite3.connect(self.__data_base_file) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    def __get_item_type_name(self, item: Item) -> str:
        if isinstance(item, Student):
            return "student"
        elif isinstance(item, Employee):
            return "employee"
        else:
            raise ValueError('Некорректный тип объекта')

    def __convert_row_to_item(self, row: sqlite3.Row) -> Item:
        item_type = row['type']

        if item_type == "student":
            item = Student()
        elif item_type == "employee":
            item = Employee()
        else:
            raise ValueError('Некорректный тип объекта')

        item.set_data(dict(row))
        return item

    def save_to_file(self, file_path: Path) -> bool:
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(self.__data_base_file, file_path)
            return True
        except Exception:
            return False

    def import_from_file(self, file_path: Path) -> bool:
        try:
            if not file_path.exists():
                return False
            shutil.copy2(file_path, self.__data_base_file)
            return True
        except Exception:
            return False

    def import_from_upload(self, file_stream):
        try:
            with open(self.__data_base_file, 'wb') as f:
                shutil.copyfileobj(file_stream, f)
            return True
        except Exception:
            return False
