# app/asm2504/st24/storage.py
import os
import uuid
import pickle
import sqlite3
from .employee import Employee
from .manager import Manager
from .director import Director
from .io_strategy import FlaskIO


class SQLiteStorage:
    def __init__(self, db_path='data/asm2504/st24/company.db'):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(employees)")
            columns = [row[1] for row in cursor.fetchall()]

            if 'data' not in columns:
                conn.execute("DROP TABLE IF EXISTS employees")

            conn.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    id TEXT PRIMARY KEY,
                    type TEXT,
                    data BLOB
                )
            ''')
            conn.commit()

    def add(self, employee):
        if not employee.id:
            employee.id = str(uuid.uuid4())
        serialized = pickle.dumps(employee)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'INSERT OR REPLACE INTO employees (id, type, data) VALUES (?, ?, ?)',
                (employee.id, employee.__class__.__name__, serialized)
            )

    def get_by_id(self, emp_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('SELECT data FROM employees WHERE id = ?', (emp_id,))
            row = cursor.fetchone()
            return pickle.loads(row[0]) if row else None

    def get_all(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('SELECT data FROM employees')
            return [pickle.loads(row[0]) for row in cursor.fetchall()]

    def get_all_formatted(self):
        employees = self.get_all()
        result = []
        for emp in employees:
            data = emp.output_data()
            data['id'] = emp.id
            data['type'] = emp.__class__.__name__
            result.append(data)
        return result

    def update_by_id(self, emp_id, employee):
        self.add(employee) 

    def delete_by_id(self, emp_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('DELETE FROM employees WHERE id = ?', (emp_id,))
            return cursor.rowcount > 0

    def clear(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('DELETE FROM employees')
            conn.commit()

    def save(self, filename):
        path = os.path.join('data/asm2504/st24', os.path.basename(filename))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(self.get_all(), f)
        return path
    
    def load(self, filename):
        import os
        import pickle
        import sys
        import types
        from .employee import Employee
        from .manager import Manager
        from .director import Director
        from .io_strategy import FlaskIO

        base_path = 'data/asm2504/st24'
        os.makedirs(base_path, exist_ok=True)

        path = os.path.join(base_path, os.path.basename(filename))
        if not os.path.exists(path):
            for ext in ['', '.pkl', '.pickle', '.dat', '.backup', '.txt']:
                candidate = path + ext
                if os.path.exists(candidate):
                    path = candidate
                    break
            else:
                print(f"Файл не найден: {filename}")
                return False

        # === Заглушки для старых классов ===
        class OldConsoleIO:
            def input_field(self, *a): return ""
            def output_field(self, *a, **kw): pass

        class OldIOStrategy: pass

        fake_modules = [
            'employee', 'manager', 'director', 'io_strategy',
            'app.asm2504.st24.employee',
            'app.asm2504.st24.manager',
            'app.asm2504.st24.director',
            'app.asm2504.st24.io_strategy',
            'storage_strategy', 'app.asm2504.st24.storage_strategy',
        ]

        original_modules = {name: sys.modules.get(name) for name in fake_modules}

        try:
            # Создаём временные модули
            for name in fake_modules:
                sys.modules[name] = types.ModuleType(name)

            for mod_name in fake_modules:
                mod = sys.modules[mod_name]
                if 'employee' in mod_name:
                    mod.Employee = Employee
                if 'manager' in mod_name:
                    mod.Manager = Manager
                if 'director' in mod_name:
                    mod.Director = Director
                if 'io_strategy' in mod_name or 'storage_strategy' in mod_name:
                    mod.ConsoleIO = OldConsoleIO
                    mod.IOStrategy = OldIOStrategy
                    mod.FlaskIO = FlaskIO

            with open(path, 'rb') as f:
                data = pickle.load(f)

            # === Адаптируем данные ===
            employees = []
            if isinstance(data, list):
                employees = data
            elif isinstance(data, dict):
                employees = list(data.values())
            else:
                print("Неизвестный формат данных")
                return False

            self.clear()
            for emp in employees:
                if not hasattr(emp, 'id') or not emp.id:
                    emp.id = str(uuid.uuid4())
                emp.io = FlaskIO()
                self.add(emp)

            print(f"Успешно загружено {len(employees)} сотрудников из старого файла: {filename}")
            return True

        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            # Восстанавливаем оригинальные модули
            for name, original in original_modules.items():
                if original is not None:
                    sys.modules[name] = original
                elif name in sys.modules:
                    del sys.modules[name]