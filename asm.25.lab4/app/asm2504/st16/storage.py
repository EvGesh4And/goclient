import pickle
import os
import sqlite3
from flask import g, current_app
from .employee import Employee
from .director import Director
from .manager import Manager


class Storage:
    def save_data(self, data):
        return NotImplementedError

    def load_data(self):
        return NotImplementedError

    def init_storage(self):
        raise NotImplementedError


class Pickle_Storage(Storage):
    def __init__(self, filename = './asm2504/st16/data.pkl'):
        super().__init__()
        self.filename = filename
        self.employees = {}

    def init_storage(self):
        self.employees = {}

    def get_next_id(self):
        if not self.employees:
            return 1
        return max(self.employees.keys()) + 1

    def add_element(self, employee):
        new_id = self.get_next_id()
        employee.id = new_id
        self.employees[employee.id] = employee

    def get_by_id(self, emp_id):
        return self.employees.get(emp_id)

    def get_employees(self):
        return list(self.employees.values())

    def update(self, employee):
        if employee and employee.id in self.employees:
            self.employees[employee.id] = employee
            return True
        return False

    def delete_employee(self, emp_id):
        if emp_id in self.employees:
            del self.employees[emp_id]

    def delete_all_employees(self):
        self.employees.clear()

    def save_data(self, data):
        data_to_save = data if data else self.employees
        try:
            with open(self.filename, 'wb') as file:
                pickle.dump(data_to_save, file)
        except Exception as e:
            print(f'Pickle save error: {e}')

    def load_data(self):
        try:
            with open(self.filename, 'rb') as file:
                loaded_data = pickle.load(file)
            if isinstance(loaded_data, list):
                self.employees = {emp.id: emp for emp in loaded_data}
            elif isinstance(loaded_data, dict):
                self.employees = loaded_data
            else:
                self.employees = {}
        except FileNotFoundError:
            self.employees = {}
        except Exception as e:
            print(f'Pickle load error: {e}')
            self.employees = {}


class SQLite_Storage(Storage):
    def __init__(self, db_path, pickle_path=None):
        self.db_path = db_path
        self.employee_classes = {'Employee': Employee, 'Manager': Manager, 'Director': Director}
        self.pickle_source_path = pickle_path
        self.table_name = 'employees'
        self.schema = None

        if not os.path.exists(self.db_path):
            self.initialize_database()

    def _get_connection(self):
        if 'db' not in g:
            g.db = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
            g.db.row_factory = sqlite3.Row
        return g.db

    def get_schema(self):
        if self.schema:
            return self.schema

        dummies = [cls(None) for cls in self.employee_classes.values()]
        schema = {}
        ignore_list = ['io', 'id']

        for dummy in dummies:
            for key, value in dummy.__dict__.items():
                if key not in ignore_list and key not in schema:
                    schema[key] = type(value)

        self.schema = schema
        return schema

    def initialize_database(self):
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except:
                pass
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        schema = self.get_schema()
        fields_sql = ["id INTEGER PRIMARY KEY AUTOINCREMENT", "type TEXT NOT NULL"]

        for field_name, field_type in schema.items():
            sql_type = "INTEGER" if field_type == int else "TEXT"
            fields_sql.append(f"{field_name} {sql_type}")

        create_stmt = f"CREATE TABLE {self.table_name} ({', '.join(fields_sql)});"

        db = sqlite3.connect(self.db_path)
        db.execute(create_stmt)
        db.close()
        print(f"DB initialized at {self.db_path}")

    def init_storage(self):
        self.initialize_database()

    def _row_to_employee(self, row):
        if not row: return None
        cls = self.employee_classes.get(row['type'], Employee)
        emp = cls(None)
        emp.id = row['id']
        for key in row.keys():
            if hasattr(emp, key):
                setattr(emp, key, row[key])
        return emp

    def get_employees(self):
        rows = self._get_connection().execute(f'SELECT * FROM {self.table_name}').fetchall()
        return [self._row_to_employee(row) for row in rows]

    def get_by_id(self, emp_id):
        row = self._get_connection().execute(f'SELECT * FROM {self.table_name} WHERE id = ?', (emp_id,)).fetchone()
        return self._row_to_employee(row)

    def extract_data(self, emp):
        schema = self.get_schema()
        data = {}
        data['type'] = emp.__class__.__name__

        for field in schema.keys():
            data[field] = getattr(emp, field, None)
        return data

    def add_element(self, emp):
        data = self.extract_data(emp)

        columns = ', '.join(data.keys())  # "type, name, age, assistant..."
        placeholders = ', '.join(['?'] * len(data))  # "?, ?, ?, ?..."
        values = list(data.values())

        sql = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        db = self._get_connection()
        cursor = db.execute(sql, values)
        db.commit()
        emp.id = cursor.lastrowid

    def update(self, emp):
        data = self.extract_data(emp)
        set_clause = ', '.join([f"{col}=?" for col in data.keys()])
        values = list(data.values())
        values.append(emp.id)

        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE id = ?"
        db = self._get_connection()
        db.execute(sql, values)
        db.commit()

    def delete_employee(self, emp_id):
        db = self._get_connection()
        db.execute(f'DELETE FROM {self.table_name} WHERE id = ?', (emp_id,))
        db.commit()

    def delete_all_employees(self):
        db = self._get_connection()
        db.execute(f'DELETE FROM {self.table_name}')
        db.execute(f'DELETE FROM sqlite_sequence WHERE name="{self.table_name}"')
        db.commit()

    def save_data(self, data):
        if not self.pickle_source_path:
            return
        helper = Pickle_Storage(filename=self.pickle_source_path)
        helper.save_data(data)

    def load_data(self):
        if not self.pickle_source_path:
            return
        helper_storage = Pickle_Storage(filename=self.pickle_source_path)
        helper_storage.load_data()
        items = helper_storage.get_employees()

        self.delete_all_employees()
        for item in items:
            item.id = None
            self.add_element(item)