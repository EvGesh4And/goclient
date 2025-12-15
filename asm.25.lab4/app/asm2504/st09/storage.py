import os
import pickle
import sqlite3
from .entity import Employee

DB_PATH = os.path.join("data", "asm2504", "st09", "employees.db")

class SQLiteStorage:
    def __init__(self, db_path: str = DB_PATH):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()
        self.columns = self._get_columns()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Создание таблицы при первом запуске."""
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    name TEXT,
                    email TEXT,
                    experience INTEGER,
                    profession TEXT,
                    department TEXT,
                    company TEXT
                )
            """)
            conn.commit()

    def _get_columns(self):
        with self._connect() as conn:
            cur = conn.execute("PRAGMA table_info(employees)")
            cols = [row[1] for row in cur.fetchall()]
        return cols   
    # --- CRUD ---
    def add_employee(self, employee):
        data = employee.to_dict()

        cols = [c for c in self.columns if c != "id"]
        placeholders = ", ".join(["?"] * len(cols))
        col_string = ", ".join(cols)

        values = [data.get(c) for c in cols]

        with self._connect() as conn:
            cur = conn.execute(
                f"INSERT INTO employees ({col_string}) VALUES ({placeholders})",
                values,
            )
            conn.commit()
            employee.db_id = cur.lastrowid

    def remove_employee(self, emp_id: int):
        with self._connect() as conn:
            conn.execute("DELETE FROM employees WHERE id=?", (emp_id,))
            conn.commit()

    def update_employee(self, emp_id: int, employee):
        data = employee.to_dict()

        cols = [c for c in self.columns if c != "id"]
        assignments = ", ".join([f"{c}=?" for c in cols])
        values = [data.get(c) for c in cols]

        with self._connect() as conn:
            conn.execute(
                f"UPDATE employees SET {assignments} WHERE id=?",
                values + [emp_id]
            )
            conn.commit()

    def clear_all(self):
        with self._connect() as conn:
            conn.execute("DELETE FROM employees")
            conn.commit()

    def get_all_entities(self, io_strategy=None):
        entities = []
        with self._connect() as conn:
            cur = conn.execute("SELECT * FROM employees")
            rows = cur.fetchall()

        for row in rows:
            data = {col: row[idx] for idx, col in enumerate(self.columns)}
            emp = Employee.from_dict(data, io_strategy)
            emp.db_id = data["id"]
            entities.append(emp)

        return entities

    # --- Pickle Import/Export ---
    def import_from_pickle(self, pickle_file="data/asm2504/st09/employees.pkl"):
        if not os.path.exists(pickle_file):
            print(f"Файл {pickle_file} не существует")
            return False
        try:
            with open(pickle_file, "rb") as file:
                pickle_employees = pickle.load(file)

            for emp in pickle_employees:
                self.add_employee(emp)

            print(f"Импортировано {len(pickle_employees)} сотрудников")
            return True
        except Exception as e:
            print(f"Ошибка импорта: {e}")
            return False

    def export_to_pickle(self, pickle_file="data/asm2504/st09/employees.pkl"):
        try:
            os.makedirs(os.path.dirname(pickle_file), exist_ok=True)
            employees = self.get_all_entities()
            with open(pickle_file, "wb") as file:
                pickle.dump(employees, file)
            print(f"Экспортировано {len(employees)} сотрудников")
            return True
        except Exception as e:
            print(f"Ошибка экспорта: {e}")
            return False
